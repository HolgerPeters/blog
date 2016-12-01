---
layout: post
category: Python
date: '2016-06-13 21:00'
modified: '2016-06-13 21:00'
status: draft
tags: 'Python, API, design'
title: The Case Against Cute APIs
---

Today, [a breach of confidentiality in let's
encrypt](https://community.letsencrypt.org/t/email-address-disclosures-preliminary-report-june-11-2016/16867)
exposed email addresses to the public. The reason for this was a
mismatch in the expectation of letsencrypt developers in how a Python
email API works, and the implementation of that API. The code in
question must have looked something like this

{% highlight python %}
from email.MIMEMultipart import MIMEMultipart
m = MIMEMultipart()

for user in users():
    m['To'] = user.email_address()
    # ...

# ...
{% endhighlight %}

Instead of changing the recipient's address in each iteration, the API
actually appends another recipient to the message object, for each
iteration, another recipient is added to the list. For letsencrypt this
means: recipients could see between between 0 and 7,618 other recipients
in the email. Now I can imagine that a mistake like this can happen
quickly, and even more quick are the usual thoughts among commenters on
the internet, that fall into statements like:

-   "This is a bug in the Python email API"
-   "This behaviour is documented and intended, if we changed it, it
    would be an interface breaking change"
-   "Even if it was documented, it is a design flaw and needs to be
    fixed"

I am not interested so much into leading this discussion. Instead, I
would like to point out the real issue behind this: *Cute* API design.

Cute APIs - The Elephant In The Room
====================================

Let's face it: When we have a look at a library (or a programming
language for that matter) our first instinct is to look at code samples.
Does ist look clean, consistent and concise? Is it maybe too verbose?
With such a superficial look at things we actually learn a good deal
about a library.

If we can read the example code, we are confident that we can write it
without too much trouble. An approachable snippet is a promise for an
approachable and easy-to-use library. While this instinct is right in
many cases, it can also fail us pretty badly.

What I call **cute apis** are APIs that are focused on such looks, they
are entirely or partially written in a way that "looks great on paper".
I am not saying that **Cute APIs** are written with malicious intent,
they are not "confidence libraries". Yet, cuteness is nothing that we
should strive for when designing an API.

What's cute about the email library example from above is the fact, that
one can add header properties just as easy as we normally set values to
a dictionary -- Overwriting the `__setkey__` interface for its class. On
first glance this looks easy, what one cannot see however is, that the
semantics of `m['To'] = "email@example.com"` are very different from
`mydict["To"] = "email@example.com"`. Not overwriting `__setkey__` to
append headers, but writing a method `add_header` would have made it
more clear that the message object accumulates headers passed to it,
unfortunately it does not look quite as snappy.

How Can We Avoid Writing cute APIs
==================================

Cute APIs are born from a mixture of intention (I want this snippet to
look great) and accident (I came up with this just after my lunchbreak
and never reviewed it critically). However there are a few alarm signs
that you can conciously watch out for when reviewing the design of an
API.

The Principle Of Least Astonishment (POLA)
------------------------------------------

When we write a new API, we are usually buried in the problem domain
quite deep already. So when we come up with an especially clever
formulation for our API, we might not realize, that its behaviour is not
intuitively understandable for the casual user (the person implementing
that 10 line script using the API, and even more so that other person
adjusting things in that script 3 years later). This is why it is
important, to be at least a bit idiomatic when implementing an API.

In the email example, expectation is that setting an element with a
`a[k] = b` form overwrites an element in a container. When the
implementation actually appends to that container instead of overwriting
an already present key/index `k`, users are surprised. By the principle
of least astonishment, we try to reduce such surprises. A custom method
with a at least somewhat descriptive name `add_header` or
`add_recipient` will not surprise so much.

Avoid Semantic Mismatches
-------------------------

The same goes for other unexpecteed tricks. Implementing common methods
from common data structures is just as bad: Like implementing a class to
have a method `append` that however does not work like `list.append` but
for example rather like `list.extend`. It is way better to give such a
method a unique name if one does not depend on making it an interface
fit for duck-typing. Avoiding semantic mismachtes is just another case
of POLA.

Don't Use The Whole Toolbelt Right Away
---------------------------------------

Write Down Type Signatures
--------------------------

Be Fearful Of Default Arguments
-------------------------------

One of the most problematic features of Python are default keyword args.
I classify this under the umbrella of *cute APIs*, because default
keyword arguments make complicated function calls look kind of simple.

For long time, I found default arguments to be kind of nice, until I
realized, that quite often they are just a convenient way to not take
decisions in API design.
