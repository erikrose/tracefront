"""Fancy traceback formatting

We have yet to decide which of these we'll do:

1. Mokeypatch the stdlib traceback module to improve traceback formatting
   everywhere.
2. Provide routines other library authors can call to print nice tracebacks.

"""
# print_exception (which is what Django uses for runserver output) and format_exception (which is what it uses for logs) seem to be the main ones. Color print_exception.
# They all call format_list or print_tb

import os
from os import getcwd, environ
from os.path import abspath
import sys
import types

from blessings import Terminal


# From pdbpp
def _import_from_stdlib(name):
    import code # arbitrary module which stays in the same dir as pdb
    stdlibdir, _ = os.path.split(code.__file__)
    pyfile = os.path.join(stdlibdir, name + '.py')
    result = types.ModuleType(name)  # TODO: switch to new
    mydict = execfile(pyfile, result.__dict__)
    return result

traceback = _import_from_stdlib('traceback')


# Steal all the stuff from the stdlib traceback module:
def _copy_to_globals(namespace, attrs):
    """Copy all the given named ``attrs`` of ``namespace`` into the global namespace."""
    g = globals()
    for attr in attrs:
        g[attr] = getattr(namespace, attr)

_copy_to_globals(traceback, traceback.__all__)


# Do this early so it's actually right. nosetests, for one, changes directory
# early in the test-running process.
_cwd = getcwd()


# Overrides of various traceback-module functions:

def format_list(extracted_list):
    """Format a list of traceback entry tuples for printing.

    Given a list of tuples as returned by extract_tb() or
    extract_stack(), return a list of strings ready for printing.
    Each string in the resulting list corresponds to the item with the
    same index in the argument list.  Each string ends in a newline;
    the strings may contain internal newlines as well, for those items
    whose source text line is not None.

    """
    # Go ahead and put the tty codes in. Usually it ends up getting printed. At
    # least that's how Django prints its tracebacks. I'm going to leave it this
    # way until it breaks something I care about. (Sentry might be a good
    # example.)
    return list(simple_format_traceback(extracted_list))


def print_tb(tb, limit=None, file=None):
    """Print up to 'limit' stack trace entries from the traceback 'tb'.

    If 'limit' is omitted or None, all entries are printed.  If 'file'
    is omitted or None, the output goes to sys.stderr; otherwise
    'file' should be an open file or file-like object with a write()
    method.

    """
    if file is None:
        file = sys.stderr

    extracted_tb = extract_tb(tb, limit=limit)

    file.write(''.join(simple_format_traceback(extracted_tb, stream=file)))


def print_list(extracted_list, file=None):
    """Print the list of tuples as returned by extract_tb() or extract_stack() as a formatted stack trace to the given file."""
    if file is None:
        file = sys.stderr
    file.write(''.join(simple_format_traceback(extracted_list, stream=file)))


# Monkeypatch our method onto the shadowed module, because the non-shadowed
# routines still look stuff up there:
traceback.format_list = format_list
traceback.print_tb = print_tb
traceback.print_list = print_list

# Use our formatting even for top-level exceptions that percolate right out of
# the interpreter:
sys.excepthook = print_exception


# End traceback-module overrides


def simple_format_traceback(extracted_tb, stream=None):
    """Call ``format_traceback()``, making up appropriate values for ``cwd`` and ``term``.

    Omitting the ``stream`` arg makes it omit tty formatting.

    """
    return format_traceback(
        extracted_tb,
        cwd='' if environ.get('TRACEFRONT_ABSOLUTE_PATHS', '').lower() in
            ('1', 'true', 'yes', 'on') else _cwd,
        term=Terminal(stream=stream),  # () makes blessings not style. Hacky.
        function_color=environ.get('TRACEFRONT_FUNCTION_COLOR', 12),
        dim_color=environ.get('TRACEFRONT_DIM_COLOR', 8),
        editor=environ.get('TRACEFRONT_EDITOR',
                           environ.get('EDITOR', 'vi')))


def format_traceback(extracted_tb,
                     cwd='',
                     term=None,
                     function_color=12,
                     dim_color=8,
                     editor='vi'):
    """Return an iterable of formatted traceback frames.

    Also include a pseudo-frame at the end representing the exception itself.

    Format things more compactly than the stock formatter, and make every
    frame an editor shortcut.

    """
    def format_shortcut(editor,
                        file,
                        line,
                        function=None):
        """Return a pretty-printed editor shortcut."""
        return template % dict(editor=editor,
                               line=line,
                               file=file,
                               function=('  # ' + function) if function else '',
                               funcemph=term.color(function_color),
                               # Underline is also nice and doesn't make us
                               # worry about appearance on different background
                               # colors.
                               plain=term.normal,
                               fade=term.color(dim_color) + term.bold)

    if not term:
        term = Terminal()

    if extracted_tb:
        # Shorten file paths:
        for i, (file, line, function, text) in enumerate(extracted_tb):
            extracted_tb[i] = human_path(source_path(file), cwd), line, function, text

        line_width = len(str(max(the_line for _, the_line, _, _ in extracted_tb)))
        template = ('  %(fade)s%(editor)s +%(line)-' + str(line_width) + 's '
                    '%(file)s%(plain)s'
                    '%(funcemph)s%(function)s%(plain)s\n')

        # Stack frames:
        for i, (file, line, function, text) in enumerate(extracted_tb):
            # extract_tb() doesn't return Unicode, so we have to guess at the
            # encoding. We guess utf-8. Use utf-8, everybody.
            yield (format_shortcut(editor, file, line, function) +
                   ('    %s\n' % (text.strip() or '').decode('utf-8')))

    # Exception:
#     if exc_type is SyntaxError:
#         # Format a SyntaxError to look like our other traceback lines.
#         # SyntaxErrors have a format different from other errors and include a
#         # file path which looks out of place in our newly highlit, editor-
#         # shortcutted world.
#         exc_lines = [format_shortcut(editor, exc_value.filename, exc_value.lineno)] + \
#                      traceback.format_exception_only(SyntaxError, exc_value)[1:]
#     else:
#         exc_lines = traceback.format_exception_only(exc_type, exc_value)
#     yield ''.join(exc_lines)


def human_path(path, cwd):
    """Return the most human-readable representation of the given path.

    If an absolute path is given that's within the current directory, convert
    it to a relative path to shorten it. Otherwise, return the absolute path.

    """
    # TODO: Canonicalize the path to remove /kitsune/../kitsune nonsense.
    path = abspath(path)
    if cwd and path.startswith(cwd):
        path = path[len(cwd) + 1:]  # Make path relative. Remove leading slash.
    return path


def source_path(path):
    """Given a path to a compiled Python file, return the corresponding source path.

    If passed a path that isn't a compiled thing, return it intact.

    """
    if path is None:
        return path
    for extension in ['$py.class', '.pyc', '.pyo']:
        if path.endswith(extension):
            return ''.join([path[:-len(extension)], '.py'])
    return path


# TODO: Maybe do the unittest-style frame-stripping stuff. Meh: the test
# framework should do that.
