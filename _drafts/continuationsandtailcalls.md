---
layout: post
category: Python
date: '2016-11-25 6:00'
modified: '2016-10-14 11:00'
slug: 'tail-call-everywhere'
tags: 'Functional Programming, Haskell, Scheme, Python'
title: Every Call A Tail Call
---

Thinking about a common pattern in Scikit-Learn machine learning
pipelines, I stumbled over a surprising link to a seemingly unrelated
optimizations in functional programming languages: *tail calls*.

# The Problem

As a rough outline, in a scikit-learn machine learning model, at one
point you have to retrieve your training data (or the one you use for
the prediction), and pass it to a model `est`, which will transform the
data and use it to train the model.

{% highlight python %}
def main():
    X, y = obtain_data()
    est = get_model()
    est.fit(X, y)
{% endhighlight %}

The *model* is usually a Pipeline object, i.e. a sequence of
transforming building blocks.

{% highlight python %}
def get_model():
    return Pipeline(ests=[Imputer(), StandardScaler(), LinearSVC()])
{% endhighlight %}

When `Pipeline.fit` is called, it loops over all of its elements and
uses each element to transform the data and pass the transformed data to
the next component, discarding the original data.

{% highlight python %}
def fit(self, X, y):
    X = self.ests[0].fit_transform(X, y)
    X = self.ests[1].fit_transform(X, y)
    X = self.ests[i].fit_transform(X, y)
    ...
    return self.ests[n].fit(X, y)
{% endhighlight %}

The variable `X` here is the *feature-matrix*, and can be a very large
object. And this makes the following observation so painful:
`fit_transform` will generally return a new object, that is roughly a
modified copy of `X`, that typically has the same number of rows than
the original feature-matrix. So when the original `X` is two gigabytes
in size, we create another object of also roughly two gigabytes. This
wouldn't be so bad, if the original `X` instance would go away. However,
is still referenced in `main`, because `X` is a local variable there,
with a reference to `X` located on the stack, that prevents the original
feature-matrix object of being collected. This means during our fit, we
just doubled the memory consumption of our model - without having any
benefit.

## Possible Fixes

# Introduction

I meant to write this blog post for a while, yet I was never sure on how
to start it. My plan is to cover a whole bunch of topics, that I didn't
know where so naturally connected to each other as they are. I decided
to roughly retrace the steps how I came to learn, that we might be able
to eliminate that backbone of our programming languages: The stack.

So this journey begins, with me trying to learn
[Scheme](https://en.wikipedia.org/wiki/Scheme_(programming_language)),
because I wanted to learn about this other paradigm *functional
programming* (and I was a little tired of learning yet another
imperative / object oriented language, because learning them seemed very
repetetive). Learning Scheme wasn't easy for me at first, but I somehow
progressed into being a Scheme *zealot* for a while.

One thing that the Scheme-tutorials I read heavily emphasized, was the
importance of recursion, as a replacement for imperative loops.
Recursion in a nutshell means, that a function calls itself, over and
over again. Of course, recursion was nothing new in general (the
mergesort algorithm can be naturally implemented using it for example):

{% highlight python %}
def mergesort(lst):
    if len(lst) == 1:
       return lst
    else:
       split = len(lst) // 2
       return merge(mergesort(lst[:split]), mergesort(lst[split:]))
{% endhighlight %}

## Example

Suppose we have a very simple function, that just adds up two numbers.
The code should be understandable, we define a function that just wraps
the `+` operator and then call this function with two numbers that are
easily recognizable later on.

{% highlight lua %}
function add_two_numbers(a, b)
    return a + b
end

add_two_numbers(33333, 44444)
{% endhighlight %}

Although lua is an interpreted language, it is compiled to bytecode
before being interpreted. Looking at the bytecode we can learn much more
about how lua will execute this small program. We can compile this with
luac -l -o test.luac test.lua to see a human readable representation of
lua bytecode:

    main <test2.lua:0,0> (7 instructions at 0x7fe3d24036b0)
    0+ params, 3 slots, 1 upvalue, 0 locals, 3 constants, 1 function
            1    [4] CLOSURE     0 0 ; 0x7fe3d2403900
            2    [2] SETTABUP    0 -1 0  ; _ENV "add_two_numbers"
            3    [7] GETTABUP    0 0 -1  ; _ENV "add_two_numbers"
            4    [7] LOADK       1 -2    ; 33333
            5    [7] LOADK       2 -3    ; 44444
            6    [7] CALL        0 3 1
            7    [7] RETURN      0 1

    function <test2.lua:2,4> (3 instructions at 0x7fe3d2403900)
    2 params, 3 slots, 0 upvalues, 2 locals, 0 constants, 0 functions
            1    [3] ADD         2 0 1
            2    [3] RETURN      2 2
            3    [4] RETURN      0 1
