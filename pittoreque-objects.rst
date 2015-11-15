==============================
Pittoresque Object Orientation
==============================

:date: 2015-10-10 20:00
:modified: 2015-10-25 13:20
:tags: python, software engineering, patterns
:category: python
:status: draft

In the imperative, object-oriented tradition, classes are
typically used for several reasons. Two of them are related
to providing abstractions: One is to implement
*polymorphism*, the property of being able to write code for
values of different types.  Another widely expressed opinion
is, to let classes encapsulate an internal, private state,
which is only accessible by public methods.

However, we also observe class usage for more mundane
reasons: Bundling often used variables in a class namespace
(which can lead to god-classes with the same problems that
global variables have in a program). And another is what I
call pittoresque object-orientation, which is about
modelling real-life objects as classes on every possible
occasion  - regardless of whether we get the benefits of
object-orientation (polymorphism and maybe state
encapsulation [#f1]_ ).

It is not that obvious that "pittoresque" object-orientation
is a problem, in fact, a lot of introductory material to
object orientation or object oriented languages in fact uses
"pittoresque" object orientation in their examples.

In this blog post I will show how "pittoresque" object
orientation can be an anti-pattern and why usage of object
orientation should focus on primarily on polymorphism,
sometimes on state encapsulation and why reduceing object
orientation to a pattern for modelling real-life objects in
software can be a bad idea.

.. [#f1] I say maybe, because I would like to reduce the
         need for state encapsulation by getting rid of
         unnecessary state in the first place.
