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

This is nice and simple.  But every code base evolves, and
so, after a few changes here (all backwards compatible
refactorings) you might find an extended version of this
function:

.. code-block:: python

   def touch(filenames):
       """kind of like coreutils touch, works for either one
       file name, or a list of file names"""

       if not isinstance(filenames, (list, iterable)):
           filenames = [filenames]

       for fname in filenames:
           with open(fname, 'a'):
               os.utime(fname, times)

What happened? For some reason, one needed "touch" several files. Probably
there was a variable containing that list of filenames. And for the
sake of convenience, the ``touch`` function has been extended to accomodate that
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
``x``'s type from its declaration). The third, and probably most important
reason to avoid this pattern is: You can just implement the
loop in the calling code instead of inside the ``touch``
function. If you need the convenience of a function that
touches a list of files, you can implement one very easily
that resorts to the first touch function:

.. code-block:: python

   def touch(filename):
       "kind of like coreutils touch"
       with open(filename, 'a'):
           os.utime(filename, times)


   def touch_many(filenames):
       for filename in filenames:
           touch(filename)

Typical cases where this (anti-)pattern in code bases
might emerge are mostly related to supporting several types
for one argument *without a direct need* [#f2]_, e.g.

* the example above using lists of elements, or a single
  element as arguments
* allowing integers/floats and strings that are implicitly
  converted to numbers
* allowing for both file-handles and strings [#f3]_

Note: Using polymorphism (object-oriented methods) in
arguments is **not** covered by this anti-pattern. So it is
perfectly fine, that ``touch_many`` can work with ``list``
values and ``Iterables``. Because here, the object system
performs the dispatch, and not a hand-rolled
``if``-statement.

Distinguishing between Procedures and Functions
===============================================

The first programming language I learned was Pascal. I do not miss it a bit,
but for one nice little nitpicking property that Pascal had.
In Pascal has two kind of *subroutines*: functions (those
that have a return value) and procedures (those without a
return value).

.. code-block:: pascal

  program Test;

  uses math, sysutils, graph;

  type
    Point = record
      x, y, z : REAL;
    end;

  function Distance(var p0, p1: Point) : REAL;
  begin
    Distance := sqrt(power(p0.x - p1.x, 2)
                   + power(p0.y - p1.y, 2)
                   + power(p0.z - p1.z, 2));
  end;

  (* calculate the angle between the lines p0-p1 and p0-p2 *)
  function TriangleAngle(var p0, p1, p2: POINT) : REAL;
  var
    InnerProd : REAL;
  begin
    InnerProd := (p1.z - p0.z) * (p2.z - p0.z)
               + (p1.z - p0.z) * (p2.z - p0.z)
               + (p1.z - p0.z) * (p2.z - p0.z);
    TriangleAngle := arccos(InnerProd / distance(p0, p1) / distance(p0, p2))
  end;

  procedure DrawTriangle(var p0, p1, p2: POINT);
  var
    angle : REAL;
  begin
    MoveTo(p1.x, p1.y);
    LineTo(p0.x, p0.y);
    LineTo(p2.x, p2.y);
    angle := TriangleAngle(p0, p1, p2);
    MoveTo(p0.x, p0.y);
    OutText(FloatToStr(angle));
  end;
  begin
   (*...*)
  end.

This distinction is only useful, when you move the
side-effectful parts of the code into procedures and the
side-effect free parts into functions. Belive it or not: if
you do this, you have a much easier time.

Even if Python does not syntactically separate functions
from procedures, we can semantically try to separate them.

Instead of conflating the calculation of the angle in a
triangle from with plotting it in a single function,
separating them along the lines of side-effectful and
side-effect-free gives you

* the opportunity to write straightforward value-oriented
  unit tests for the side-effect free function
  ``TriangleAngle``
* life is easier when writing an alternative implementation
  of the side-effectful code, for example using another
  drawing library, etc.

In essence, this is a classic separation of concerns: The
piece of code, that prints out an angle does not
need to know how it is calculated.

How to tell apart Functions from Procedures
-------------------------------------------

You can get the best benefits from separating functions from procedures if you
are able to tell them apart rather quickly browsing through your code.

First of all, if you can help it, don't return values from
procedural functions. Moreover, if you do return a value,
make sure that your function does not mutate your arguments.

.. code-block:: python

   # this is bad: mutates lst, doesn't appear to work
   # in-place on first glance, but it actually does.
   def replace_none_items(lst, replacement):
       for i, elem in enumerate(lst):
           if elem is None:
               lst[i] = replacement
       return lst

   # better, does not pretend to be a function, still works
   # in-place, still a # "procedure"
   def do_replace_none_itemsr(lst, replacement):
       for i, elem in enumerate(lst):
           if elem is None:
               lst[i] = replacement

   # best: a real function, either as list comprehension or
   # by just mutating a local variable
   def replace_none_items(lst, replacement):
       res = []
       for elem in lst:
           if elem is None:
               res.append(replacement)
           else:
               res.append(elem)

   def replace_none_items_list_comprehension(lst, replacement):
       def replace_none(x):
           if x is None:
               return replacement
           else:
               return x
       return [replace_none(elem) for elem in lst]

   # and if you find the list comprehension to be hard to read:
   def replace_none_items2(lst, replacement):
       for elem in lst:
           if elem is None:
               yield replacement
           else:
               yield elem


Avoid Awkwared Arguments
========================

Python is really liberal on function arguments. This is great, but can turn out
to be a magnet for trouble if not used with care. In fact there I have several
anti-patterns regarding arguments that I can demonstrate here, and I encourage
you to take some extra time when writing your functions to not write these kind
of functions in the first place.


Flag Parameters
---------------

Some arguments make a function do one thing in one case, and a completely other
thing in the other case. Typically booolean arguments are the most often
offendes, but this is not limited to them.

.. code-block:: python

   def determine_estimated_download_size(url, cached=False):
       if cached:
           # ....
           return
       else:
           # ....
           return

In most cases, I would refactor both branches of the if statement into their
own function and possibly move the if-statement to the calling code. In more
cases than you would belive, the flag parameter ``cached`` is actually known at
compile time and the calling code can directly call into the cached, or the
not-cached implementation. If not, one can still leave the flag-parameter
function in place as a dispatcher, or one might have a valid use case for
*classes*.


Default Arguments
-----------------

Default arguments to functions are a curse and a blessing. They are a blessing
because they can make a programmer's life much more easy. Use carefully chosen
defaults unless you have reason to override them - sounds like a good approach.
However, one can also look at them as an indicator for lazy design. In the end,
they can easily expose implementation detail to the function user and make
refactoring a lot harder. They take away the direct need for the programmer to
carefully design their interfaces (a "just add a default argument and we are
fine" attitude will bite you later).

A few questions to ask yourself when introducing default arguments:

* will changing the default value of a keyword argument be an interface
  breaking change?
* are there combination of arguments with overridden defaults that are
  contradictory?


Final Thoughts
==============

When thinking of ways to structure your code

* focus on **intent** (intent, not indent)
* prefer simple functions
* try to avoid incidental state
* instead of trying to offer convenient interfaces, strive
  for clear, robust interfaces


Footnotes
=========


.. [#f1] It took me a while to figure out that the
         Zen of Python is filed under the "humour" section on the python
         homepage. Naturally it should be taken with a grain of salt.

.. [#f2] Polymorphism is not a bad thing *per se*, it just
         should not be used lightly and it is best used
         using classes and not using if-statements.

.. [#f3] Issue here: how is the file going to be opened.
