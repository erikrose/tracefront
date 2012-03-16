===========
Exceptional
===========

It makes your tracebacks look like this::

  Traceback (something useful here):
    vi +44 noseprogressive/tests/test_integration.py  # test_error
      self._count_eq('ERROR: ', 2)
    vi +17 noseprogressive/tests/test_integration.py  # _count_eq
      eq_(str(self.output).count(text), count)
    vi +31 /Users/erose/kitsune/lib/python2.6/site-packages/tools.py  # eq_
      assert a == b, msg or "%r != %r" % (a, b)
  AssertionError: 1 != 2

* Judicious use of color and other formatting makes the traceback easy to scan.
  It's especially easy to slide down the list of function names to keep your
  place while debugging.
* Using relative paths (optional) and omitting redundant wording fits much more
  in limited screen space.
* Editor shortcuts (see below) let you jump right to any problem line in your
  editor.

Editor Shortcuts
----------------

For each frame of a traceback, exceptional provides an editor shortcut.
This is a combination of a filesystem path and line number in a format
understood by vi, emacs, the BBEdit command-line tool, and a number of other
editors::

  vi +361 apps/notifications/tests.py  # test_notification_completeness

Just triple-click (or what have you) to select the line, and copy and paste it
onto the command line. You'll land right at the offending line in your editor
of choice. As a bonus, the editor shortcut is more compact than the stock
traceback formatting, which is handy if you have something like a test runner
printing a lot of them. If it looks like the output is going to a capable
terminal, it'll even use color.

You can set which editor to use by setting either of these, which exceptional
checks in order:

* The ``EXCEPTIONAL_EDITOR`` environment variable
* The ``$EDITOR`` environment variable


Installation
============

Just do this... ::

    pip install exceptional

...and all your tracebacks will be pretty and helpful.


How It Works
============

Exceptional shadows the stock traceback module, calling through for most stuff
but replacing the core formatting bits. If a program makes assumptions about
the composition of formatted tracebacks, it might break, but that would be
weird, since there are more convenient representations easily available.


License
=======

Exceptional is under the MIT License. See the LICENSE file.


Version History
===============

1.0
    * Pulled the traceback formatting stuff out of `nose-progressive`_.

.. _`nose-progressive`: http://pypi.python.org/pypi/nose-progressive/
