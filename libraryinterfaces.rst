===========================================
Things to consider before writing a library
===========================================

:date: 2016-04-10 22:00
:tags: python, engineering, software
:category: python
:status: draft


At first it seems straightforward: that code you are writing
seems useful for other developers and projects, too. Why not
write a library, prevent the wheel from being reinvented
again and solving matters once and for all?

Then, things become complicated. Users complain about a
complex interface, the first bug reports complaining about
interface breaking changes arrive in an issue tracker and
all of the sudden you realize, that you can either fix that
corner case bug at the core of your library, by introducing
an interface breaking change, or not fix it to not anger the
library users who are - probably - not running into that
corner case.

Long story short: Writing libraries requires you to make
choices, which wouldn't bother you at all while writing a
program. Unfortunately, best practices on how to write great
libraries are rare or rather not as fashionable as many
other topics. Yet here it is, an overview of best practices
and some anti-patterns to avoid when writing a library (and
some advice on when to avoid writing a library, and when to
pursue it).

Golden Rules for Writing a Library
==================================

A checklist:

- A library should do things in one domain, and that domain
  only.

- A library should implement functionality at a certain
  abstraction level. High-level and low-level functionality
  should be cleanly separated.

- A library should be conservative about introducing
  dependencies.

- The essential aspect of a library is its public interface.
  It should be carefully chosen, functions, classes and
  instance attributes should be private by default.

- By publishing a library, library developers take over
  responsibility. This responsibility requires commitment to
  those that depend on the library.

- The public interfaces are untouchable.

- Proper versioning and managing change are crucial for the
  long-term success of a library (and hapiness of users).
  Maintainers should be prepared to maintain features
  indefinitely.

Obviously Bad Ideas
===================

Some anti-patterns are so bad, that I do not even want to
write too lengthy about it.

Multi-Purpose Libraries
-----------------------

Multi-purpose libraries can be really bad. I am sure some of
your artefacts pull in one or the other. `logilab-common
<https://pypi.python.org/pypi/logilab-common/>`_ comes
to my mind, and maybe to some extend, also `py
<http://pylib.readthedocs.org/en/latest/>`_ [#f1]_ .

As a rule of thumb, if a library works on two different
domains, or on different abstraction levels, it is a smell.

I usually don't like to call out bad behavior, and I mention
these examples here only, to show you that smart people can
easily fall into this trap. Reasons why people write
multi-purpose libraries include (non-exhaustive):

- perceived obligation to follow `DRY`_
- fear of a maintenance overhead for several libraries.
- fear of integration problems (with a monolith, managing
  dependencies is easier)
- perceived benefit of sharing "low-level" code among
  library functionalities. Two components both need some XML
  tooling, it is tempting to put those two, and the XML tool
  into one multi-purpose library.

The actual problem with multi-purpose libraries is, that
they have a tendency for feature creep (you'll have a hard
time arguing that a feature is out-of-scope for that
library, if it has already accumulated a lot of features),
the coupling of unrelated code removes all semantic from
versioning. And the worst: auxilliary functionality which
should not be part of the public interface has a tendency to
become public interface eventually.

Cauliflower-Libraries, or: Someone might find this useful
---------------------------------------------------------

This anti-pattern is similar to the multi-purpose library in
many ways, although even single-purpose libraries can suffer
from this anti-pattern. Imagine you write a library for
parsing of a certain file format. While implementing this
library, you have written a heuristics to guess character
encodings and MIME types of embedded files. It is good code
and you are proud of it. So why should this functionality be
available to your users only indirectly when they read in a
file? Wouldn't it be great if they could use your function
whenever they want to check whether some data is an HTML
or an XML document?

This is tempting, but just think about the consequences. If
this functionality is part of your public interface, it is
much harder to change it without breaking an interface. As
long as it is an implementation detail of the parser (see
`Leaking Implementation`_)


DRY
===

DRY, "Don't repeat yourself" is one of those recommendations
that would have fared better with a worse slogan. DRY is
just too catchy and often the actual recommendation behind
dry is lost.

        "Every piece of knowledge must have a single,
        unambiguous, authoritative representation within a
        system."

This means, that DRY  is about reducing redundancy and
contraries in your code base. It is not DRY to define your
SQL scheme once in your database migration scripts, and a
second time in your ORM layer. Or if your mailserver defines
a maximal attachement size, you only have one corresponding
configuration option, which is used by all parts of the
system checking attachment sizes.

DRY is not about reducing code duplication at all cost.

Leaking Implementation
======================

Some implementation details cannot be hidden, in a way, some
properties of your functionality can be considered to be a
public interface, although no such promise was ever made.
For example, imagine  that a change to your implementation
increases execution times by a magnitude (although it does
not change signatures). Would this be an acceptable,
non-interface breaking change? Only for so long as users do
not depend on execution times of previous versions of your
software.

User:
    The new version of library X has become so much slower
    when reading XML files.
Library Developer:
    Yes, we now validate it more carefully.
User:
    But that means, that I cannot upgrade to the new version
    of the library.
Library Developer:
    Oh I am sorry, we never promised to not check data more
    thoroughly. We need these checks if only for security
    reasons.
User:
    But what shall I do now?

There is no one way on how to handle such a situation. It is
unpleasant for library users and developers alike. Remember,
as a library developer you have a responsibility for the
users, and in many cases, responsibilities can stand in
conflict. If you try to prevent leaking implementation
details in the first place, you should try to reduce the
public interface to a well-defined set of functions /
classes.

Footnotes
=========

.. [#f1] Ironically, my favorite test runner ``py.test`` has
   been born inside of ``pylib``.

