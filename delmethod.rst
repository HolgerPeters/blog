======================================================
An Interesting Fact About The Python Garbage Collector
======================================================

:date: 2016-02-16 20:34
:modified: 2016-02-16 20:34
:tags: Python, Interpreter
:category: python

While Python prides itsself of being a simple, straightforward programming
language and being explicit is pointed out as a core value, of course, one
can always discover interpreter specifics and implementation detail, that
one did not expect to find when working at the surface. These days I learned
more about a peculiar property of the Python garbage collector, that I would
like to share.

Let's start by introducing the problem quickly. Python manages its objects
primarily by reference counting. I.e. each object stores how many times it
is referenced from other places, and this reference count is updated over
the runtime of the program. If the reference count drops to zero, the object
cannot be reached by the Python code anymore, and the memory can be
freed/reused by the interpreter.

An optional method ``__del__`` is called by the Python interpreter when the
object is about to be destroyed. This allows us to do some cleanup, for
example closing database connections, etc. Typically ``__del__`` rarely has
to be defined. For our example we will use it to illustrate when the disposal of an object happens:

.. code-block:: python

   >>> class A(object):
   ...     def __del__(self):
   ...         print("no reference to {}".format(self))
   ...
   >>> a = A()
   >>> b = a
   >>> c = a

The situation in memory resembles this schematic::

	┌────┐
	│ a  │────────────┐
	└────┘            ▼
	┌────┐    ┌───────────────┐
	│ b  │───▶│A() refcount=3 │
	└────┘    └───────────────┘
	┌────┐            ▲
	│ c  │────────────┘
	└────┘

Now we let the variables ``a``, ``b``, and ``c`` point to ``None`` instead
of the instance ``A()``:

.. code-block:: python

   >>> a = None
   >>> b = None
   >>> c = None
   No reference to <__main__.A object at 0x102ace9d0>

Changing the situation to::

	┌────┐    ┌────┐
	│ a  │─┬─▶│None│
	└────┘ │  └────┘
	┌────┐ │  ┌───────────────┐
	│ b  │─┤  │A() refcount=0 │
	└────┘ │  └───────────────┘
	┌────┐ │
	│ c  │─┘
	└────┘


After we have overwritten the last reference (``c``) to our instance of
``A``, the object is destroyed, which triggers a call to ``__del__`` just
before really destroying the object.

Cyclic References
-----------------

However, there are instances where the reference count cannot simply go down
to zero, it is the case of cylic references::

          ┌────┐
          │ a  │
          └────┘
             │
             ▼
     ┌───────────────┐
  ┌──│A() refcount=2 │◀─┐
  │  └───────────────┘  │
  │  ┌───────────────┐  │
  └─▶│B() refcount=1 │──┘
     └───────────────┘

Setting ``a`` to ``None``, we will still have refcounts of ``>= 1``. For
these cases, Python employs a garbage collector, some code that traverses
memory and applies more complicated heuristics to discover unused objects.
We can  use the ``gc`` module to manually trigger a garbage collection run.

.. code-block:: python

   >>> a = A()
   >>> b = A()
   >>> a.other = b
   >>> b.other = a
   >>> a = None
   >>> b = None
   >>> import gc
   >>> gc.collect()
   11

However, since ``A`` implements ``__del__``, Python refuses to clean them,
arguing that it cannot not tell, which ``__del__`` method to call first.
Instead of doing the wrong thing (invoking them in the wrong sequence),
Python decides to rather do nothing -- avoiding undefined behaviour, but introducing a potential memory leak.

In fact, Python will not clean any objects in the cycle, which can possibly
render a huger group of objects to pollute memory (see
https://docs.python.org/2/library/gc.html#gc.garbage ). We can inspect the
list of objects, which could not be garbage collected:

.. code-block:: python

   >>> gc.garbage
   [<__main__.A object at 0x102ace9d0>, <__main__.A object at 0x102aceb10>]

Finally, if you remove the ``__del__`` method from the class, you would not
find these objects in ``gc.garbage``, as Python would just dispose of them.

Python 3
--------

As it turns out, from Python 3.4 on, the issue I wrote about does not exist
anymore. ``__del__`` s do not impede garbage collection any more, so
``gc.garbage`` will only be filled for other reasons. For details, you can
read `PEP 442 <https://www.python.org/dev/peps/pep-0442/>`_ and the `Python docs <https://docs.python.org/3.5/library/gc.html#gc.garbage>`_.

Considering the adoption of Python 3.4, most Python code bases have to be
careful about when to use ``__del__``.
