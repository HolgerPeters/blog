---
layout: post
category: 'Data-Science'
date: '2016-08-05 20:00'
modified: '2016-08-05 20:00'
status: draft
tags: 'Data-Science'
title: Disecting the gravest mistake in interpreting probabilities
---

Bayes Theorem
=============

The last equation can be solved for $\wp(A\mid B)$ by dividing through
$\wp(B)$ and we obtain a very famous equation in probability theory,
Bayes' theorem

$$\wp(A\mid B)  = \frac{\wp(B \mid A)\wp (A)}{\wp(B)}$$

To this day, I am always amazed at how easily this theorem can be
derived from basic rules of probability. Given Bayes' theorem's
controversial history, and importance for Bayesian statistics.

The most-common statistical mistake
===================================

Often when Bayes' theorem is discussed, the discussion quickly
concentrates on the roles of individual terms in this equation, the
likelihood $\wp(B\mid
A)$, and the prior $\wp(A)$, and fully marginalized likelihood[^1]
$\wp(B)$. But even if you don't use Bayes' theorem in practice, you
should take a closer look at it for a moment, because it will tell you
how you can avoid one of the most common mistakes when dealing with
probabilities and statistics. Here it comes:

> When $\wp(A)\neq \wp(B)$, then
>
> $$\wp(A\mid B) \neq \wp(B \mid A)$$

In plain english, with our example of the wet street: *The probability
for a wet street, under the condition that it rained is not equal to the
probability for rain, under the condition of a wet street, unless the
probability for a wet street is equal to the probability for rain.*

Example: Implications from using a drug test
--------------------------------------------

We are interested in the odds of an individual being a drug user $D=1$,
given that a drug-test is positive $P=1$. We know that in the whole
population, we have with $\wp(D=1)=\frac{1}{200}$ a moderate probability
for an individual being a drug user.

We also know, that the test has a type I error of 1%, i.e. $\wp(P=1\mid
D=0) = \alpha = \frac{1}{100}$. And we similarly assume a type II error
with $\wp(P=0\mid D=1) = \beta = \frac{1}{100}$. Using Bayes' rule we
can calculate the posterior odds for begin a drug user against not being
a drug user, under the condition that the test is negative.

$$O(D=1:D=0 \mid P=1) = \frac{\wp(P=1 \mid D=1)}{\wp(P=1 \mid D=0)} O(D:\neg D)$$

We choose calculate $\frac{\wp(P=1 \mid D=1)}{\wp(P=1 \mid D=0)} =
\frac{0.99}{0.01}$ and from the above assumption $O(D:\neg D)= 1:
199$. We then obtain posterior odds of $O(D=1:D=0) = 99:199\approx 1
: 2$, and in probability space $\wp(D=1 \mid P=1) \approx \frac{1}{3}$
and $\wp(D=0 \mid P=1) \approx \frac{2}{3}$.

Likelihood-Maximization
-----------------------

If we infer the likelihood $\wp(\mathcal{D}\mid \mathcal{M})$, the
probability for data $\mathcal{D}$ given a model $\mathcal{M}$ using a
maximum-likelihood approach, we do not necessarily maximize the
posterior $\wp(\mathcal{M}\mid \mathcal{D})$.

[Maximum a-posteriori
method](https://www.wikiwand.com/en/Maximum_a_posteriori_estimation) is
a thing though.

The Coin Flip
-------------

Now that we have settled that $\wp(A\mid B) \neq \wp(B\mid A)$, but for
corner cases, I want to convince you that Bayes' theorem is a honking
great idea.

Suppose you are flipping a coin multiple times. Normally you would
assume $\wp(H)=\mu=0.5$, but this coin you flip seems somewhat biased,
and you want to infer from several throws, what this coin's bias $\mu$
is. We'll assume that you have data
$\vec{x} = (0, 1, 0, 0, 1, 0, \ldots)$. And you want to infer the
probability for that parameter $\mu$ given your data:
$\wp(\mu\mid\vec{x})$. Or rather, since we know that the individual coin
flips are independent, we can just use the number of observed
head-throws $k$ and the total number of experiments $n$ and determine
$\wp(\mu \mid n, k)$. Using Bayes' theorem we can express this as

$$\wp(\mu\mid n, k) = \frac{\wp(k \mid n, \mu) \wp(n, \mu)}{\wp({k,n})}$$

Obtaining the probability for a model (the left-hand side), given the
data is non-trivial. I wouldn't know where to start, but with Bayes'
theorem. On the right-hand side, we find $\wp(x\mid n, \mu)$, the
likelihood[^2], and if we think about it more closely, we can determine
this likelihood! We look for the probability of throwing head n out of k
times, given an indivdual probability $\mu$ for throwing head. This is
the [Binomial
Distribution](https://www.wikiwand.com/en/Binomial_distribution).

$$\wp(k \mid n,\mu) = \text{Binomial}(k \mid n, \mu) = \binom{n}{k} \mu^k(1-\mu)^{n-k}$$

### The Tricky Denominator

We could then go on by solving the Prior $\wp(n, \mu) = \wp(\mu \mid n)
\wp(n) = \wp(\mu)\wp(n)$, since we know that the probabilitiy for $\mu$
is independent of the number of trials $n$. The denominator of bayes'
theorem is notoriously difficult to obtain. It is most commonly called
*evidence*, yet I prefer the term *fully marginalized likelihood*[^3]
which describes better what it is. It can be obtained by calculating the
integral over the model parameter $\mu$

$$\wp(k, n) = \int\limits_0^1 \mathrm{d}\mu\ \wp(k \mid n, \mu) \wp(n) \wp(\mu)$$

But instead of trying to integrate this equation, we just utilize that
the binomial-likelihood works exceptionally well together with
beta-distributed priors $\wp(\mu) = \text{Beta}(\mu \mid s_0, f_0)$.

### Calculate your Posterior with this one, weird trick

With beta-distributed priors
$\wp(\mu) = \text{Beta}(\mu \mid s_0, f_0)$, bayes' theorem simplifies
to a very simple update-equation.

$$\text{Beta}\left(\mu \mid s_0 + s, f_0 + (n-s)\right) = \text{Binomial}\left(s \mid n, \mu \right) \text{Beta}\left(\mu\mid s_0, f_0 \right)$$

Here we have substituted $k \to s$, and $n \to s + f$ (which stand for
failure and success).

[^1]: <https://twitter.com/jakevdp/status/760510916928663552>

[^2]: The likelihood is a probability (or probability density) for data
    under the condition of a model.

[^3]: <https://twitter.com/jakevdp/status/760510916928663552>
