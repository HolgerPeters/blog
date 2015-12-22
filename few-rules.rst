==================================================
Improve your Python code with these N simple steps
==================================================

:date: 2015-10-10 20:00
:modified: 2015-10-25 13:20
:tags: testing, python
:category: python
:status: draft

.. _zenofpython: https://www.python.org/doc/humor/#the-zen-of-python

Python, like Ruby/Javascript/Lua or any other dynamically typed programming
language, is quite liberal when it comes to how you lay out your program.
Although the zenofpython_  suggests that "There should be one -- and preferably
only one -- obvious way to do it." [#f1]_ There are no simple rules that can be
blindly followed. However, over time I learned a few tricks that might help you
writing legible, maintainable and testable Python code.


Don't support too many types
============================

This is something that I stumble over quite a lot. A function might start out
supporting one argument (is a string object for example).

.. code-block:: python

   def touch(filename):
       "kind of like coreutils touch"
       with open(filename, 'a'):
           os.utime(filename, times)

And after a while, the function suddenly looks like this:

.. code-block:: python

   def touch(filenames):
       """kind of like coreutils touch, works for either one file name, or a list
       of file names"""

       if not isinstance(filenames, (list, iterable)):
           filenames = [filenames]

       for fname in filenames:
           with open(fname, 'a'):
               os.utime(fname, times)

What happened? For some reason, one needed "touch" several files. Probably
there was a variable somewhere containing that list of filenames. And for the
sake of convenience, the touch function has been extended to accomodate that
use case.

This is a bad pattern for a number of reasones. First of all, the touch
function starts to become filled up with "trivial" argument processing logic.
This wouldn't be so bad, if it wouldn't overshadow those two lines that do the
actual work. For a reader new to the code base, it will be harder to read about
how files are "touched". Then, you stop being able to infer types of variables
that are passed to ``touch`` as arguments. When ``touch`` only supported a
string, if you saw a call ``touch(x)``, you could be kind of sure that ``x``
was a string. With the more liberal version of ``touch``, one cannot make that
inference any more (because there are no type declarations in Python, this is
obviously more handy than in - let's say - C++ where we typically know of
``x``'s type from its declaration). And the third, and probably most important
reason to avoid this pattern is: You can just implement the loop in a separate
function:

.. code-block::

   def touch(filename):
       "kind of like coreutils touch"
       with open(filename, 'a'):
           os.utime(filename, times)


   def touch_many(filenames):
       for filename in filenames:
           touch(filename)

Typical cases of this anti-pattern in code bases can be:

* using lists of elements, or a single element as arguments (like the example)
* allowing integers/floats and strings that are implicitly converted to numbers
* allowing for both file-handles and strings [#f3]

Note: Using polymorphism (object-oriented methods) in arguments is **not** covered by
this anti-pattern. So it is perfectly fine, that ``touch_many`` can work with
``list`` values and ``Iterables``.

Distinguishing between Procedures and Functions
===============================================

The first programming language I learned was Pascal. I do not miss it a bit,
but for one nice little nitpicking property that Pascal had. In Pascal, there
was a difference between functions (with a return value) and procedures
(without a return value):

.. code-block:: pascal

  function add(x: integer, y: integer) : integer;
  begin
      add := x + y
  end

  procedure DrawRectangle(x0, y0, x1, y1: integer);
  begin
      DrawLine(x0, y0, x0, y1);
      DrawLine(x0, y0, x1, y0);
      DrawLine(x1, y0, x1, y1);
      DrawLine(x1, y1, x1, y1);
  end



.. [#f1] It took me a while to figure out that the
         Zen of Python is filed under the "humour" section on the python
         homepage. Naturally it should be taken with a grain of salt.

.. [#f3] Issue here: how is the file going to be opened.
