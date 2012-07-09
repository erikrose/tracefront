# -*- coding: utf-8 -*-
"""Tests for traceback formatting."""

# Putting this up here so the line numbers in its tracebacks don't change much

def one():
    """Raise a mildly interesting exception."""
    def two():
        h = []
        h[1]
    two()

def _tb():
    """Return a mildly interesting traceback."""
    return _triple()[2]


def _triple():
    """Return a (type, value, tb) triple."""
    try:
        one()
    except IndexError:
        return exc_info()
    else:
        raise AssertionError('We should have had an IndexError.')


from os import chdir, getcwd, environ
from os.path import dirname, basename
from StringIO import StringIO
from sys import exc_info

from blessings import Terminal
from nose import SkipTest
from nose.tools import eq_, ok_

from traceback import (format_traceback, human_path, source_path, format_list,
                       extract_tb, print_tb, print_exception, print_list)


syntax_error_tb = ([
     ("setup.py", 79, '?', """classifiers = ["""),
     ("/usr/lib64/python2.4/distutils/core.py", 149, 'setup', """dist.run_commands()"""),
     ("/usr/lib64/python2.4/distutils/dist.pyc", 946, 'run_commands', """self.run_command(cmd)"""),
     ("/usr/lib64/python2.4/distutils/dist.pyo", 966, 'run_command', """cmd_obj.run()"""),
     ("/usr/lib/python2.4/site-packages/setuptools/command/install$py.class", 76, 'run', """self.do_egg_install()"""),
     ("/usr/lib/python2.4/site-packages/setuptools/command/install.py", 100, 'do_egg_install', """cmd.run()"""),
     ("/usr/lib64/python2.4/urllib2.py", 580, 'proxy_open', """if '@' in host:""")
     # Was originally TypeError: iterable argument required
    ], SyntaxError, SyntaxError('invalid syntax', ('/Users/erose/Checkouts/nose-progress/noseprogressive/tests/test_integration.py', 97, 5, '    :bad\n')))
attr_error_tb = ([
     ("/usr/share/PackageKit/helpers/yum/yumBackend.py", 2926, 'install_signature', """self.yumbase.getKeyForPackage(pkg, askcb = lambda x, y, z: True)"""),
     ("/usr/lib/python2.6/site-packages/yum/__init__.py", 4309, 'getKeyForPackage', """result = ts.pgpImportPubkey(misc.procgpgkey(info['raw_key']))"""),
     ("/usr/lib/python2.6/site-packages/rpmUtils/transaction.py", 59, '__getattr__', """return self.getMethod(attr)"""),
     (__file__, 69, 'getMethod', """return getattr(self.ts, method)""")
    ], AttributeError, AttributeError("'NoneType' object has no attribute 'pgpImportPubkey'"))

environ['EDITOR'] = 'vi'


def test_human_path():
    chdir(dirname(__file__))
    eq_(human_path(__file__, getcwd()), basename(__file__))  # probably fails in Jython


def test_source_path():
    eq_(source_path('thing.py'), 'thing.py')
    eq_(source_path('thing.pyc'), 'thing.py')
    eq_(source_path('thing.pyo'), 'thing.py')
    eq_(source_path('thing$py.class'), 'thing.py')
    eq_(source_path('/all/your/thing.pyc'), '/all/your/thing.py')


def test_syntax_error():
    """Special handling of syntax errors should format nicely and not crash."""
    raise SkipTest
    options = dict(term=Terminal(stream=StringIO()))
    f = ''.join(format_traceback(*syntax_error_tb, **options))
    assert f.endswith(
        """vi +97  /Users/erose/Checkouts/nose-progress/noseprogressive/tests/test_integration.py
    :bad
    ^
SyntaxError: invalid syntax
""")


def test_non_syntax_error():
    """Typical error formatting should work and relativize paths."""
    raise SkipTest
    options = dict(term=Terminal(stream=StringIO()))
    f = ''.join(format_traceback(*attr_error_tb, **options))
    print f
    print repr(f)
    eq_(f, """  vi +2926 /usr/share/PackageKit/helpers/yum/yumBackend.py  # install_signature
    self.yumbase.getKeyForPackage(pkg, askcb = lambda x, y, z: True)
  vi +4309 /usr/lib/python2.6/site-packages/yum/__init__.py  # getKeyForPackage
    result = ts.pgpImportPubkey(misc.procgpgkey(info['raw_key']))
  vi +59   /usr/lib/python2.6/site-packages/rpmUtils/transaction.py  # __getattr__
    return self.getMethod(attr)
  vi +69   {this_file}  # getMethod
    return getattr(self.ts, method)
AttributeError: 'NoneType' object has no attribute 'pgpImportPubkey'
""".format(this_file=source_path(__file__)))


def test_empty_tracebacks():
    """Make sure we don't crash on empty tracebacks.

    Sometimes, stuff crashes before we even get to the test. pdbpp has been
    doing this a lot to me lately. When that happens, we receive an empty
    traceback.

    """
    list(format_traceback(
        [],
        AttributeError,
        AttributeError("'NoneType' object has no attribute 'pgpImportPubkey'")))


def test_unicode():
    """Don't have encoding explosions when a line of code contains non-ASCII."""
    raise SkipTest
    unicode_tb = ([
         ("/usr/lib/whatever.py", 69, 'getMethod', """return u'あ'""")
        ], AttributeError, AttributeError("'NoneType' object has no pants.'"))
    ''.join(format_traceback(*unicode_tb))


# Untested thus far:
# Colors


def test_format_list():
    expected_list = [
        u'  \x1b[90m\x1b[1mvi +21 traceback/tests.py\x1b(B\x1b[m\x1b[94m  # _triple\x1b(B\x1b[m\n    one()\n',
        u'  \x1b[90m\x1b[1mvi +11 traceback/tests.py\x1b(B\x1b[m\x1b[94m  # one\x1b(B\x1b[m\n    two()\n',
        u'  \x1b[90m\x1b[1mvi +10 traceback/tests.py\x1b(B\x1b[m\x1b[94m  # two\x1b(B\x1b[m\n    h[1]\n']
    eq_(format_list(extract_tb(_tb())), expected_list)


def test_print_tb():
    expected_string = u"""  vi +21 traceback/tests.py  # _triple
    one()
  vi +11 traceback/tests.py  # one
    two()
  vi +10 traceback/tests.py  # two
    h[1]
"""
    out = StringIO()
    print_tb(_tb(), file=out)
    eq_(out.getvalue(), expected_string)


def test_print_list():
    expected_string = u"""  vi +21 traceback/tests.py  # _triple
    one()
  vi +11 traceback/tests.py  # one
    two()
  vi +10 traceback/tests.py  # two
    h[1]
"""
    out = StringIO()
    print_list(extract_tb(_tb()), file=out)
    eq_(out.getvalue(), expected_string)


def test_rebinding():
    """Make sure our new print_tb gets called by the routines we didn't patch."""
    out = StringIO()
    options = dict(file=out)
    print_exception(*_triple(), **options)
    value = out.getvalue()
    # Make sure the old formatting isn't happening:
    ok_('File "' not in value)
    # Make sure *some* kind of traceback is in there:
    ok_('Traceback (most recent call last):' in value)


# TODO: Mock out env vars and cwd so tests aren't dependent on my env.
# TODO: Format exceptions nicely.
