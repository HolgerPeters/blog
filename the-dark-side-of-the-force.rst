=======================================
Exceptions - The Dark Side of the Force
=======================================

:date: 2016-01-13 23:16
:tags: Python, Clean Code, Best Practice
:category: python
:summary: A recent blog post `"If you don't like exceptions, you don't like Python" <http://stupidpythonideas.blogspot.de/2015/05/if-you-dont-like-exceptions-you-dont.html>`__ has made rounds lately, and compelled me to write a partial rebuttal.  It is not like that blog post is completely wrong, but it is not the be-all and end-all of this topic. And if I may add, it is kind of opinionated.



A recent blog post `"If you don't like exceptions, you don't
like Python" <http://stupidpythonideas.blogspot.de/2015/05/if-you-dont-like-exceptions-you-dont.html>`__ has made rounds lately, and
compelled me to write a partial rebuttal. It is not like
that blog post is completely wrong, but it is not the be-all
and end-all of this topic. And if I may add, it is kind of
opinionated.

The original article states that exceptions are central to
Python, that the common advice "exceptions should only be
for errors, not for normal flow control" is wrong, goes on,
explaining that exceptions are used in core implementations,
such as the iterator protocol, and attribute access, thus
that they are a central feature of the language.  Some
longer parts of the blog posts are concerned debunking
commonly held misconceptions by Java and C++ programmers.

Roughly speaking, exceptions in this article are portrait
very favourably, with all that praise, all criticism and
questions regarding their use are eclipsed.


Use exceptions for error handling
---------------------------------

This is a point where I just whole-heartedly agree with
barnert. Errors should be propagated using exceptions, so

.. code-block:: python

   def min(*lst):
       if not lst:
          raise ValueError("min(..) requires a list with at least one element")
       minimum = lst[0]
       for item in lst:
           if minimum > item:
               minimum = item
       return minimum

is a perfectly fine usage of exceptions, and callers should
check for these exceptions if their code does not guarantee
that the argument is a list of length above 0.


Exceptions are dissociated from values and variables
----------------------------------------------------
Sometimes I stumble over code that uses a pattern like this:

.. code-block:: python

   result = []
   result.append(dosomething(bar))
   try:
      foo = bar[key][anotherkey]
      res = dosomething(foo)
      result.append(res[evenanotherkey])
   except KeyError:
      ....
   finally:
      return result

This snippet has many exception-related issues and shows how
not to use exceptions. First of all, it is unclear which
key-access in the try block does raise the exception. It
could be in ``bar[key]``, or in ``_[anotherkey]``, then in
``res[evenanotherkey]``, or finally it could happen in
``dosomething(foo)``. The exception mechanism dissociates
error handling from the values and variables. My question
is: can you tell whether catching KeyErrors from
``dosomething()`` is intended?

So when using exceptions, one has to be really careful about
which exceptions are caught and which aren't. With defensive
programming (i.e.  ``haskey()``)-style checks, it is
unambiguous and hardly as "intrusive" to the code as writing
out individual ``try-catch`` blocks for each indexing
operation.


Exceptional Dangers
~~~~~~~~~~~~~~~~~~~

So there are basically two risks when using exceptions:

1. An exception that should be caught is not caught
2. An exception is caught wrongfully

The first risk is definitely a risk, but one that I don't
worry too much about.  The second is a risk I definitely
fear. How many functions in your code can throw
``KeyErrors``, ``ValueError``, ``IndexError``,
``TypeError``, and ``RuntimeError`` can your code throw?


Exceptions as Pythonic gotos
----------------------------

Exceptions can emulate goto statements. Of course they are
jumps to upper levels on the stack, but also within
statements. In C code, goto's are a primary means of
function-local control flow and error handling (and for
error-handling, they are rather uncontroversial):

.. code-block:: c

   int
   max_in_two_dim(double * array, size_t N, size_t M, double *out) {
     if (N * M == 0)
        goto empty_array_lbl;
     double max = array[0];
     for (int i=0; i < N; ++i) {
         for (int j=0; j < M; ++j) {
           double val = array[j * N +k];
           if (val != val) // NaN case
              goto err_lbl;
           if (max < val)
              max = val;
         }
     }
     return 0;
     nan_lbl:
       fprintf(stderr, "encountered a not-a-number value when unexpected");
       return -1;
     empty_array_lbl:
       fprintf(stderr, "no data in array with given dims");
       return -2;
   }

You can model this usage with exceptions in Python. I have
seen such code in the wild.


.. code-block:: python

   def whatever(arg1, arg2):
     try:
         for i in range(N):
             for j in range(M):
               # ..
               if ...:
                  raise RuntimeError("jump")
         return out
     except RuntimeError:
       # cleanup
       # ..

In most cases there are ways to avoid this pattern that are
preferrable.  Python's for loops have an optional ``else``
branch that helps avoiding such jumps. Nevertheless, this
pattern can go awry with a ``RuntimeError`` happending at
some other place in the loop, etc.


Meta: Ingroup, Outgroup Thinking
--------------------------------

What I disklike the most about barnert's article is probably
mostly what one can read in the title: "If ..., you don't
like Python". It is in line with a lot of talk I hear about
code/software/solutions being "Pythonic". What this seems to
imply is, that must take sides: Either you are in line with
an orthodox Python community, or you are an outsider,
someone who is not "Pythonic" enough. All of this is not
helpful for improving code.

Conclusion
----------
Exceptions are a central and powerful tool in Python. But
use them with care and caution. Do not pretend that they are
like a magic wand, don't use them to show your love for
python. Use them when the individual situation calls for
exception usage.
