===========
Exceptional
===========

It makes your tracebacks look like this::

  Traceback (something useful here):
    vi +44 noseprogressive/tests/test_integration.py  # test_error
      self._count_eq('ERROR: ', 2)
    vi +17 noseprogressive/tests/test_integration.py  # _count_eq
      eq_(str(self.output).count(text), count)
    vi +31 /Users/erose/Virtualenvs/kitsune/lib/python2.6/site-packages/nose/tools.py  # eq_
      assert a == b, msg or "%r != %r" % (a, b)
  AssertionError: 1 != 2

You can copy and paste any of those lines to jump right to the offending frame
in your editor. These are also more compact than the stock tracebacks (which is
handy if you have something like a test runner printing a lot of them).

If it looks like the output is going to a capable console, it'll even use color.


Installation
============

Just do this... ::

    pip install exceptional

...and all your tracebacks will be pretty and helpful.


How It Works
============

Exceptional shadows the stock traceback module.
