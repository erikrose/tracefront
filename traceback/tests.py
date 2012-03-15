# -*- coding: utf-8 -*-
"""Tests for traceback formatting."""

from os import chdir, getcwd
from os.path import dirname, basename
from StringIO import StringIO

from blessings import Terminal
from nose.tools import eq_

from traceback import format_traceback, human_path, source_path


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
    f = ''.join(format_traceback(*syntax_error_tb, term=Terminal(stream=StringIO())))
    assert f.endswith(
        """vi +97  /Users/erose/Checkouts/nose-progress/noseprogressive/tests/test_integration.py
    :bad
    ^
SyntaxError: invalid syntax
""")


def test_non_syntax_error():
    """Typical error formatting should work and relativize paths."""
    f = ''.join(format_traceback(*attr_error_tb, term=Terminal(stream=StringIO())))
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
    unicode_tb = ([
         ("/usr/lib/whatever.py", 69, 'getMethod', """return u'あ'""")
        ], AttributeError, AttributeError("'NoneType' object has no pants.'"))
    ''.join(format_traceback(*unicode_tb))


# Untested thus far:
# Colors