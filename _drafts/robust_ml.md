---
layout: post
category: 'Data-Science'
date: '2018-05-10 19:54'
modified: '2018-05-10 19:54'
status: draft
tags: 'Data-Science'
title: Robust Machine Learning
---

John D. Cook recently
[blogged about robust statistical models](https://www.johndcook.com/blog/2018/05/08/robust-statistics-2/), he
writes

> P. J. Huber gives three desiderata for a statistical method in his book Robust Statistics:
>
> 1. It should have a reasonably good (optimal or nearly
>    optimal) efficiency at the assumed model.
> 2. It should be robust in the sense that small deviations
>    from the model assumptions should impair the
>    performance only slightly.
> 3. Somewhat larger deviations from the model should not
>    cause a catastrophe.

Now this got me thinking, what does robustness mean in terms
of a machine learning model? Huber's desirables for a
a statistical method aren't completely off for ML models.
But let's take the perspective of a consumer of the model's
predictions, because this is where a lack of robustness will
hurt the most.

From a business point of view, we use machine learning
because we want to obtain the machine learning model's
prediction in follow-up work flows. In fact, such a
prediction may be just a small input to a more complex
process. What means robustness for this consumer?

* the prediction's errors shouldn't increase substantially
  over time (unless you have a deterministic problem)
* the predictive service should not fail (unless you have a deterministic problem)

Typical sources of errors are:

* timing issues (variations in computation times)
* data availability issues (external data services may not
  be available or internal data delivery may be delayed)
* data variation


# Missing Data Sources

A machine learning pipeline may draw and integrate data from
several sources, both internal and external. Each of these
sources has a probability for being unavailable and can thus
put the success of the prediction run at risk. Imagine
scenarios like

* a geolocation service from an external provider is
  unavailable due to network reasons
* one of the databases with complementary core data is
  temporarily unavailable due to hardware failures

_How can we deal with such situations on the model level?_
Generally, we cannot just omit data in the prediction step,
that we used for fitting a model. So when the data is
unavailable, we either have to abort the prediction, or
fall back on an alternative, simpler model, that gives less
accurate, but acceptable results. This means that it can be
better to hand off the result of an under-fitting model than
not provide prediction results at all.

# Variation in Data

This aspect is probably very close to Huber's argument on
robustness. In machine learning applications, we usually
apply cross-validation to empirically test whether the model
is overfitting. However, this cross-validation is still
happening in a limited data set, and in a predictive
service, the data used as input for a prediction step, and
potentially the training data (when the models are retrained
frequently) will vary over time and can introduce problems.

## Bounding Prediction Output

A measure to avoid a catastrophe (or at least to prevent it
from causing huge problems) is to constrain prediction
results to a plausible value range. For regression problems
this often means to cut off value ranges below zero (or to
avoid them by log-transforming the target variable). If the
boundaries are not as clear, at least a bound for an order
of magnitude should be introduced. For example, if your
regression targets range from 0 to 1000, you might want to
constrain prediction results to the $$ 0< x <10000 $$ , so
don't end up very unrealistic predictions values of
$$10^7$$.

You might want to introduce an alerting for out-of-bounds
prediction values, so that you can consider retraining the
model or adjusting the bounds if need be.

## Adversarial Data

Adversarial data points are a special category with regards
to robustness. One aspect of machine learning that is coming
more and more into focus is that of security. It has been
demonstrated, that machine learning models can be tricked
into predictin certain results, when they are fed with
curated data sets.

# Timing Issue

Various stages of a machine learning pipeline may not
finish on time. This is true for data procured from external
sources, but even more so from local database queries.
Iterative algorithms may take another round, depending on
the termination criterium.

One way of reducing this risk is by doing as much work as
possible in advance once it is still not time critical.
