==========
Tracefront
==========

.. image:: https://secure.travis-ci.org/erikrose/tracefront.png?branch=master
   :target: http://travis-ci.org/erikrose/tracefront

**Note: This is a still an early pre-release. It works for me except for some
ugliness with SyntaxErrors, but there are no guarantees.**

Tracefront makes your tracebacks pretty and useful, like in `nose-progressive`_:

.. image:: https://github.com/erikrose/nose-progressive/raw/master/in_progress.png

(The FAIL bits and test names, of course, are just part of that testrunner.)

What's my motivation?

* Judicious use of color and other formatting makes the traceback easy to scan.
  It's especially easy to slide down the list of function names to keep your
  place while debugging.
* Using relative paths (optional) and omitting redundant wording fits much more
  in limited screen space.
* Editor shortcuts (see below) let you jump right to any problem line in your
  editor.

Editor Shortcuts
----------------

For each frame of a traceback, Tracefront provides an editor shortcut.
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

You can set which editor to use by setting either of these, which Tracefront
checks in order:

* The ``$TRACEFRONT_EDITOR`` environment variable
* The ``$EDITOR`` environment variable


Installation
============

Just do this... ::

    pip install tracefront

...and all your tracebacks will be pretty and helpful for any app that does
this::

    imports traceback

In the future, I'm thinking about using even deeper evil to make it active even
more implicitly.


Options
=======

Tracefront is configured by setting environment variables.

``TRACEFRONT_ABSOLUTE_PATHS=1``
    Set this to 1 to always use absolute paths rather than ones relative to the
    current working directory.
``TRACEFRONT_EDITOR=<editor>``
    The editor to use when building editor shortcuts
``TRACEFRONT_FUNCTION_COLOR=<0..15>``
    ANSI color number to use for function names in tracebacks
``TRACEFRONT_DIM_COLOR=<0..15>``
    ANSI color number to use for de-emphasized text (like editor shortcuts) in
    tracebacks


How It Works
============

Tracefront shadows the stock traceback module, calling through for most stuff
but replacing the core formatting bits. If a program makes assumptions about
the composition of formatted tracebacks, it might break, but that would be
weird, since there are more convenient representations easily available.


License
=======

Tracefront is under the MIT License. See the LICENSE file.


Version History
===============

0.3 (2012-03-22)
    * Grab the current working directory earlier so we're more likely to get
      the relative paths right (like when running nosetests).
    * Whip tox into shape. Tests now pass under Python 2.5.
    * Install more thoroughly. This should catch tracebacks thrown by the
      interpreter itself, not just ones explicitly formatted--as long as the
      program imports the traceback module at some point.
    * Patch print_list(), the last major routine that needed to be prettified.
      We still need to polish up display of the last few lines of SyntaxErrors.

0.2 (2012-03-17)
    * Use terminal codes all the time. (Django uses format_list instead of
      print_tb, but I want it to be in color anyway.)
    * Document all the options in the readme.

0.1 (2012-03-16)
    * Pulled the traceback formatting stuff out of `nose-progressive`_. Barely
      tested at all. Will probably erase your drive.

.. _`nose-progressive`: http://pypi.python.org/pypi/nose-progressive/
