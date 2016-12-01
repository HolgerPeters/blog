---
layout: post
category: 'Data-Science'
date: '2016-08-19 02:00'
modified: '2016-08-19 02:00'
status: draft
tags: 'Data-Science'
title: Dissecting Code Is Documentation
---

Every other month I stumble over a discussion about whether "code is
documention" is misguided or genious advice. The classical sides in this
debate are the "code is the single source of truth" side and the "code
cannot replace documentation" side. However, if the question is debated
with these two outcomes in mind it usually is a bit too shallow and so
these discussions often lose track and miss the real opportunity that is
in the "code is documentation" mantra. So in this blog post I aim at
dissecting this conflict to show you how self-documenting code and
documentation are complimentary things.

The first thing to realize about documentation is, that documentation
always has an audience. A user-manual for example is directed at users,
a developer's handbook at developers. The reference manual probably at
both with a focus on experienced users. An generated API/module
documentation of an application must be focused on the only API consumer
that is there: the programmer, and the API/module documentation of a
library is focussed on the library consumer.

Manuals and documentation pages are great to get started. Manuals are
texts, that are often meant to be read linearly, this is a benefit
because the reader can avoid jumping back and forth and concentrate on
reading, but it can also be a drawback, because one might have to read
long texts before finding relevant information.

In contrast, API docs are all about documenting components in isolation.
The reader of an API doc will jump back and forth in the docs, use links
and a search function to query for documentation. This can lead the
reader quickly to the information they look for, but they are not so
great at describing the interplay of such components.

Already we can conclude, that "Code is documentation" can never be about
the documentation with the user as an audience, it is always about
documentation for a developer working on this artefact. "Code is
documentation" is focussed on the implementation details of a code-base.

Discrepancies between Code and Documentation
============================================

I am pretty sure you have been in a situation like this several times in
your life. You read documentation, that states something about the
software, and at the same time, you see that the software seems to
contradict the documentation, either doing things differently or not at
all, or doing things that the documentation explicitly said it wouldn't.
Reasons for this could be

-   documentation for the feature is older than the implementation, i.e.
    when changing the implementation, the documentation was not updated
    (very typical)
-   implementation and documentation didn't match to begin with.
-   documentation and code are based on a specification, yet code and
    documentation interpret that specificiation differently.

Since documentation can usually not be tested, this issue is a very
likely one. Using the "code is documentation" strategy might help you
with the implementation-documentation-discrepancy problem, because it
tries to elevate the code to a single-source of truth and free the
programmer from this double-entry bookkeeping, always having to look for
documentation that might have to be changed, when performing a change in
the code-base.

What can we document in code?
=============================

A simple example for code that doesn't live by the "code is
documentation" motto, could look like the following implementation of
the popular "FizzBuzz" problem:

``` {.sourceCode .python}
def fizz_buzz(n):
    # for all integer numbers smaller than n
    for i in xrange(n):
        # if i is divisible by 3 and 5
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        # if i is divisible by 3
        elif i % 3 == 0:
            print("Fizz")
        # if i is divisible by 5
        elif i % 5 ==0:
            print("Buzz")
        # all other cases, just print out the number
        else:
            print(i)
```

At first sight you might think that this is a nicely documented piece of
code, but actually it is not so great.

Some comments, like the one just above the `for` loop and the one above
the `else` statement are not providing any added value to the code. The
for i in range idiom is typically explained within the first 3 chapters
of a Python book, so every programmer who has basic familiarity with
Python will know it, even more so do programmers know that an `else` in
an if-statement is executed for all cases not matched by the condition.
And indeed, stripping the snippet of these comments does not decrease
its readability:

``` {.sourceCode .python}
def fizz_buzz(n):
    for i in xrange(n):
        # if i is divisible by 3 and 5
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        # if i is divisible by 3
        elif i % 3 == 0:
            print("Fizz")
        # if i is divisible by 5
        elif i % 5 ==0:
            print("Buzz")
        else:
            print(i)
```

Now we have 3 remaining comments. They describe the usage of the modulo
operator for testing divisibility. This is not a bad idea, because not
every programmer might be confident in reading expressions with the
modulo operator `%`. However, we could also solve this by introducing
variables

``` {.sourceCode .python}
def fizz_buzz(n):
    for i in xrange(n):
        is_divisible_by_3 = i % 3 == 0
        is_divisible_by_5 = i % 5 == 0

        if is_divisible_by_3 and is_divisible_by_5:
            print("FizzBuzz")
        elif is_divisible_by_3:
            print("Fizz")
        elif is_divisible_by_5:
            print("Buzz")
        else:
            print(i)
```

Now we have eliminated all comments, while we keep their information in
the source code, they are now in the variable names. The if-statements
can be read very naturally and can be understood even if you haven't
thought through why you can use the modulo operator to test for
divisibility.

But we can do even better! Right now, we have extracted low-level
information (the modulo stuff) from the if-statement, but it is still in
our function. If we introduce a function to care for divisibility, we
could move the low-level code out of the function:

``` {.sourceCode .python}
def is_divisible(i, n):
    """
    Returns True if i is divisible by n, otherwise returns False.

    Paramters
    ---------
    i
        dividend
    n
        divisor:
    """
    return i % n == 0
```

But can we make the code easier to understand, so that we don't need to
depend on a docstring for understanding the function? Yes we can

``` {.sourceCode .python}
def is_divisible(dividend, divisor):
    rest = dividend % divisor
    return rest == 0
```

our fizzbuzz procedure now looks simplified and high-level:

``` {.sourceCode .python}
def is_divisible(dividend, divisor):
    rest = dividend % divisor
    return rest == 0

def fizz_buzz(n):
    for i in xrange(n):
        if is_divisible(i, 3) and is_divisible(i, 5):
            print("FizzBuzz")
        elif is_divisible(i, 3):
            print("Fizz")
        elif is_divisible(i, 5):
            print("Buzz")
        else:
            print(i)
```

As a last step, we could start to separate the generation of the string
that should be printed from the code that loops.

``` {.sourceCode .python}
def is_divisible(dividend, divisor):
    rest = dividend % divisor
    return rest == 0

def test_is_divisible():
    assert is_divisible(15, 3) == True
    assert is_divisible(15, 5) == True
    assert is_divisible(15, 4) == False
    assert is_divisible(3, 3) == True
    assert is_divisible(3, 2) == False

def fizz_buzz_term(i):
    if is_divisible(i, 3) and is_divisible(i, 5):
       return "FizzBuzz"
    elif is_divisible(i, 3):
       return "Fizz"
    elif is_divisible(i, 5):
       return "Buzz"
    else:
       return str(i)

def test_fizz_buzz_term():
    assert fizz_buzz_term(3) == "Fizz"
    assert fizz_buzz_term(9) == "Fizz"
    assert fizz_buzz_term(3**10) == "Fizz"
    assert fizz_buzz_term(5) == "Buzz"
    assert fizz_buzz_term(5 * 4) == "Buzz"
    assert fizz_buzz_term(5 * 4 * 3) == "FizzBuzz"
    assert fizz_buzz_term(5 * 3**10) == "FizzBuzz"
    assert fizz_buzz_term(8) == "8"
    assert fizz_buzz_term(19) == "19"

def fizz_buzz(n):
    """Prints out numbers from 0 to n - 1, however, printing "Fizz" for
    numbers divisible by 3 and "Buzz" for numbers divisible by 5, and
    "FizzBuzz" for numbers divisible by 3 and 5."""
    for i in xrange(n):
        print(fizz_buzz_term(i))
```

I am pretty sure, some might consider that last transformation to be
overkill, but consider the benefits

1.  We now have 3 functions that have exactly one purpose
2.  Functions is\_divisible and `fizz_buzz_term` are easily unit
    testable! The first implementation of FizzBuzz was not at all
    unit testable.
3.  The functions are now simpler and shorter
4.  Naming values is harder than naming functions, using functions, we
    avoid having to search vor variable names.
5.  It is now very easy to implement variations of fizz buzz. For
    example, the fizz-buzz list generator
    `[fizz_buzz_term(i) for i in xrange(100]`.
6.  Now that we have abstracted `is_divisible`, we can lay it out in a
    way that it is more readable than the very compact
    `(i % 3) == 0` notation.

The mantra "code is documentation" is not one that says "I can avoid
documentation", rather it is one that says "I can document for my fellow
developer (and future me) by writing the code in a way that it is
accessible, and understandable, and the best place to do this is the
code, functions and identifiers themselves instead of writing long
comments.

"code is documentation" can also help you when arguing whether certain
changes to the code base are necessary. For example, when a function has
a name, that does not fit what it does, that function should be renamed.
Your coworker might however be against it, arguing that this would mean
changing the whole code-base, that it was too dangerous for little
benefit, and that one might just leave a comment in the source and leave
things be. Seeing code as a source of documentation helps me make a
point for correcting that function's name, even if it requires some
effort, because a few weeks from now, a bug might be left unnoticed
because the function name was wrong.

Finding the right place to document things
==========================================

Suppose you
