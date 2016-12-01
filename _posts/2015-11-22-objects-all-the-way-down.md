---
layout: post
category: python
date: '2015-11-22 23:12'
modified: '2015-11-22 23:14'
summary: |
    After researching [the backgrounds of Python's unittest
    module](http://www.holger-peters.de/why-i-use-pytest.html) I got curious
    about [Smalltalk](http://en.wikipedia.org/wiki/Smalltalk), one of the
    first truly object-oriented programming languages. I looked into it
    (more specific, I played around with [Pharo](pharo)) and if you like,
    this blog post will take you along this journey using a [Rosetta
    Stone](https://en.wikipedia.org/wiki/Rosetta_Stone) approach by writing
    Python and Smalltalk snippets next to each other.
tags: 'Python, Smalltalk, Pharo, Programming Languages'
title: Objects All The Way Down
permalink: objects-all-the-way-down.html
---

After researching [the backgrounds of Python's unittest
module](http://www.holger-peters.de/why-i-use-pytest.html) I got curious
about [Smalltalk](http://en.wikipedia.org/wiki/Smalltalk), one of the
first truly object-oriented programming languages. I looked into it
(more specific, I played around with [Pharo](pharo)) and if you like,
this blog post will take you along this journey using a [Rosetta
Stone](https://en.wikipedia.org/wiki/Rosetta_Stone) approach by writing
Python and Smalltalk snippets next to each other.

Smalltalk was first released in 1972 and I was surprised when I realized
how advanced and radical its take on object-orientation is. It seems
more advanced than a lot of today's languages in a lot of aspects.

I'll just start by introducing you to Smalltalk's syntax by comparison
with the most common syntax elements:

{% highlight haskell %}
class MyClass(object):
    def a_methodcall(x):
        a = list(range(10, 1, -1))
        a.sort()
        return a
{% endhighlight %}

And now the implementation of the method in Smalltalk (for the class
definition see[^1])

{% highlight smalltalk %}
MyClass>>aMethodCall
     |a|
     a := (10 to: 1 by: -1) asArray
     ^ a sort
{% endhighlight %}

First of all, the code is not that different. We create a list of values
from 10, 9, ... to 1 in Python which we convert to a list object. In
Smalltalk, we do the same, however, we do not invoke a function like
range, but we call the `to:by:` method of the integer class (think of
this as if we called `10.to_by(to=1, by=-1)` in Python). Calling a
method `asArray` then converts an intermediate representation of the
range into an array. Finally, we sort the list calling the `sort` method
of the Array object in Smalltalk, just as we sort the list in Python
calling the same method. The Smalltalk representation then returns the
result of the sort using its return operator `^`, as does the Python
version using `return`.

So far we have seen that Python and Smalltalk are kind of similar,
although Smalltalk has a funny way of naming and calling methods,
dispersing method arguments over the method name `10 to: 1 by: -1`.

Every value is an object, every operation a method call
=======================================================

The next snippet shows how Smalltalk really treats everything as an
object, radically. Take the following class `User` with a method that
returns a string representation for that user (maybe this is what a UI
would display then). If a username is undefined, it will return a string
that identifies the user as an anonymous user, otherwise it will
directly return the user name.

{% highlight haskell %}
class User(object):
    def repr_name(self):
         "Return the name of the user if available, otherwise 'anonymous user'"
         if self.name is None:
             res = "anonymous user"
         else:
             res = self.name
         return res

class User2(object):
    def repr_name(self):
         return "anonymous user" if self.name is None else self.name
{% endhighlight %}

They translate directly into two Smalltalk methods[^2]

{% highlight smalltalk %}
User>>getRepresentativeName
    "I return the name of the user if available, otherwise 'anonymous user'"
    |res|
    name == nil
        ifTrue:  [res := 'anonymous user']
        ifFalse: [res :=  name].
    ^ res
{% endhighlight %}

and in a more functional style with an evaluating expression:

{% highlight smalltalk %}
User2>>getRepresentativeName
    "I return the name of the user if available, otherwise 'anonymous user'"
    ^ name == nil
        ifTrue: 'anonymous user'
        ifFalse: name.
{% endhighlight %}

So the boolean class of Smalltalk has methods `ifTrue:ifFalse`,
`ifTrue`, etc. that can replace a special syntax for conditionals like
the one Python has. Using the same approach (implementing methods), we
can also write list-comprehension-style expressions -- with the
difference that in Smalltalk no special syntax is necessary. This
example here is a solution for the [first project euler
problem](https://projecteuler.net/problem=1):

{% highlight smalltalk %}
divisibleRange := (1 to: N - 1) select: [ :i | i % 3 = 0 or: [ i % 5 = 0 ] ].
sumOfMultiples := divisibleRange inject: 0
                                 into: [ :subTotal :item | subTotal + item ].
{% endhighlight %}

{% highlight haskell %}
divisible_range = (i for i in range(1, N) if i % 3 == 0 or i % 5 == 0)
from functools import reduce # needed for python 3 (WTF)
sum_of_multiples = reduce(lambda sub_total, item: sub_total + item,
                          divisible_range,
                          0)
{% endhighlight %}

I won't withhold, that I am pretty delighted at the fact, that Smalltalk
is so flexible, that it can express stuff like list-comprehension, loops
and conditionals in a similar, but probably more readable way like
Python, however with fewer and simpler syntax elements. I particularly
find Smalltalk's method-based syntax `inject:into:` to be one of the
most readable ways to formulate a `reduce` operation[^3].

Object Oriented But On Which Level?
===================================

So far we have seen mostly, that Smalltalk chooses sending "messages"
(Smalltalk lingo for "calling methods") for a lot of cases where
languages like Python implement special syntax. We have also seen that
this special syntax is not necessarily more powerful than Smalltalk's
message-based approach. On the other hand, apart from having less syntax
elements to learn, it might not be immediately obvious whether
Smalltalk's approach is more beneficial or less beneficial than the
custom-syntax one.

Let us consider an example, Python has this interesting property (call
it a hack or feature according to taste) that you can define a
`__bool__` method for your class (Python 3, `__nonzero__` in Python 2).
In the if statement, it seems that Python calls `bool(obj)`, which in
the following case then dispatches to `obj.__bool__`:

{% highlight haskell %}
class Test:
    def __bool__(self):
        return True

if Test():
   print("hello")  # <- is executed
{% endhighlight %}

compare this to an established "overloading":

{% highlight haskell %}
if "":
   print("hello")  # <- is not executed
else:
   print("world")  # <- is executed
{% endhighlight %}

The whole approach of Python is kind of weird here, nevertheless, the
result is that types can define for themselves how they are interpreted.
Using Smalltalk's object-oriented approach, it is quite clear that
overloading the `ifTrue:ifElse:` message suffices at achieving such a
behaviour. This is definitely simpler than Python's approach[^4]

But what can we take from that? I have concluded, that the
object-oriented approach, that I had previously considered to be
concerned with architecture, i.e. the interplay of various code units.
In languges like Python, Java and C++, there is a tendency of writing
object-oriented code in the large and structured programming code within
the methods. In Smalltalk, I can see how object-orientation can also be
used within these units. At this micro-level, some properties of
object-oriented programming that I am not fond of, such as
state-encapsulation become less and less important, which resonates with
my preference of functional programming patterns.

Getting Rid of Source Files
===========================

Another interesting (and radical) take on software development in
Smalltalk is its approach to source files. In short: Smalltalk is
usually not edited in source files. Instead, the IDE is not only the
editor that you open files in, but instead it is more of a source code
database that stores objects and methods in an image file.

Obviously, this approach never took hold, to this day, we are editing
code in source files. Nevertheless, it was the inspiration for the IDEs
we know today, like Eclipse, Pycharm, etc.

![In Smalltalk, editing takes place in a central IDE with a class and
method browser.](assets/images/smalltalk-as-ide.png)

Ian Bicking has two blog posts that identify this as the reason why
Smalltalk did not catch on
([one](http://www.ianbicking.org/where-smalltalk-went-wrong.html) and
[two](http://www.ianbicking.org/where-smalltalk-went-wrong-2.html)). I
am not sure if this was the reason back then in the 80ies, but I do
think that this might be a reason in the Github-driven software world
today.

Conclusions
===========

The Smalltalk ecosystem looks dated. If you google for information,
you'll stumble over a lot of pages that seem to come right from the
90ies. Some of those go at great lengths of explaining concepts of
Smalltalk to C programmers, which is tiresome if you are already used to
dynamic, object-oriented typing.

Working in an image conflicts with my typical usage of version control
while programming, which kind of rules out Smalltalk for me.

What surprised me about Smalltalk is, how many 'functional' elements the
language has. It is actually less awkward to write a lambda function in
Smalltalk than in Scheme or Common Lisp, and the core APIs of the
built-in classes seem to rely on them heavily as well.

I had seen object-orientation as an architectural feature of programming
languages, meaning that I considered object-orientation to be more about
structuring code on a larger scale, and not about structuring it on the
level within a function/method level. Looking at Smalltalk I gained a
better understanding on how object-oriented concepts can be used on all
scopes.

In a way the interesting part about this comparison is the question
whether a minimal, expressive syntax is preferable over a specialized,
more complex syntax, that is fine-tuned for convenience. I'll just leave
the judgment up to you, just remember the [Zen of
Python](https://www.python.org/doc/humor/#the-zen-of-python)'s words:
"Readability counts. Special cases aren't special enough to break the
rules.".

But if you are curious, go on and download [Pharo](pharo) and check it
out.

Obligatory Footnotes
====================

[^1]: To help you read along these snippets: The caret `^` is
    Smalltalk's `return`, the `[...]` sections are "blocks", comparable
    to anonymous functions or indented parts in Python:

    A class is declared in Smalltalk in the class browser. The
    declaration is actually a method call on the superclass. I.e.
    creating a subclass `User` involves calling the
    `subclass:instanceVariableNames:classVariableNames:category` method
    on the superclass `Object`.

        Object subclass: #User
            instanceVariableNames: 'name'
            classVariableNames: ''
            category: 'blogexample'

    Since messages (methods) are also written in the object browser,
    they are not syntactically associated with the object declaration
    (not in the way as python defines methods by having them indented in
    the class definition).

    A conventional way of showing class association of object names is
    to write `ClassName>>messageName`. I did this in the snippets. If
    you write them in the Pharo System Browser, you should ignore the
    `ClassName>>` part when entering the message.

[^2]: To help you read along these snippets: The caret `^` is
    Smalltalk's `return`, the `[...]` sections are "blocks", comparable
    to anonymous functions or indented parts in Python:

    A class is declared in Smalltalk in the class browser. The
    declaration is actually a method call on the superclass. I.e.
    creating a subclass `User` involves calling the
    `subclass:instanceVariableNames:classVariableNames:category` method
    on the superclass `Object`.

        Object subclass: #User
            instanceVariableNames: 'name'
            classVariableNames: ''
            category: 'blogexample'

    Since messages (methods) are also written in the object browser,
    they are not syntactically associated with the object declaration
    (not in the way as python defines methods by having them indented in
    the class definition).

    A conventional way of showing class association of object names is
    to write `ClassName>>messageName`. I did this in the snippets. If
    you write them in the Pharo System Browser, you should ignore the
    `ClassName>>` part when entering the message.

[^3]: Although the Bdfl [is known to dislike reduce
    altogether](http://www.artima.com/weblogs/viewpost.jsp?thread=98196)
    (markup is mine):

    > So now `reduce()`. This is actually the one I've always hated
    > most, because, apart from a few examples involving `+` or `*`,
    > almost every time I see a `reduce()` call with a non-trivial
    > function argument, I need to grab pen and paper to diagram what's
    > actually being fed into that function before I understand what the
    > `reduce()` is supposed to do. So in my mind, the applicability of
    > `reduce()` is pretty much limited to associative operators, and in
    > all other cases it's better to write out the accumulation loop
    > explicitly.

    I think they are actually better than a spelled-out accumulation
    loop, because typically in a code-base that accumulation loop will
    soon be stuffed with lot's of other code that has nothing to do with
    the accumulation and it can become quite hard, even with pen and
    paper, to be sure to understand what that loop does.

[^4]: In the case of true-false, the principle here is called
    truthiness, which by itsself might be debatable. I probably would
    rather have the programmer explicitly state the intention of a
    string being not empty instead of implicitly relying on a
    "truthiness" setting.
