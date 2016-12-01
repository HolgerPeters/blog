---
layout: post
category: 'Data-Science'
date: '2016-09-22 23:07'
modified: '2016-09-22 23:07'
status: draft
tags: 'Data-Science'
title: Simple incident statistics with one simple trick
---

Have you ever caught yourself feeling edgy when someone said "five out
of ten people ....", because you felt that this was a fraction that
could be reduced to the much simpler "1 out of 2" people? Working with
ratios and fractions conditioned me in this way at least. However, when
it comes to statistics, there is information in "5 out of 10", that
would be lost by expressing it as "1 out of 2". And fortunately we can
utilize this information for better insights and judgements.

I recently observed an issue where I had a CI job not reaching a remote
server. This didn't happen only once. When I had a look at the last 20
runs, that were not collected by the log rotation, I counted about 3
failurs in 20 runs. In this situation I was unsure whether I should
start doing something about this, or rather wait whether it was just a
random coincidence. A very simple way to get some understanding about
these numbers is to simply calculate a failure rate of

$$\frac{3}{20}=0.15$$

This number by itsself doesn't tell us much. Of course it seems that the
failures were not extremely rare, but also not very frequent. If we had
recorded 30 failurs in 200 runs, I would have been sure that there was a
problem, and if we had had only one failure in ten runs, I wouldn't have
spent too much time hunting an issue, that might never occur again. But
with 3 failurs in 20 runs, I was kind of unsure how to proceed. What
helped me was applying Bayesian reasoning to the problem. And this is
what I'll show in this blog post.

We can quickly learn a bit more about the situation using the beta
distribution. The beta distribution describes how a success-probability
is distributed, when a certain number of successful cases and a certain
number of failure-cases has been observed. We use the Beta-distribution
from `scipy`, and use it with the number of failures $\alpha=3$, and the
number of successes $\beta=20-3=17$.

Using scipy, we can instantiate an object representing a beta
distribution and inspect its properties with the number of failures and
successes from our example of failing CI jobs (I'll explain later in
this article, what the values of one-half mean, that I added ontop of
$\alpha$ and $\beta$). We are especially interested in the mean and the
standard deviation of the beta-distribution:

{% highlight python %}
>>> from scipy.stats import beta
>>> dist = beta(3 + 0.5, 17 + 0.5)
>>> dist.mean()
0.16666666666666666
>>> dist.std()
0.07945521577046602
{% endhighlight %}

This gives us a mean failure rate of $0.17\pm 0.08$. So using the beta
distribution, we not only get a rate alone, but also a uncertainty for
this value. By this, we learn that it would also be reasonable, that the
failure rate is as low as $0.05$ or much higher, like $0.35$. Overall,
the standard deviation is not extremely small, but also not extremely
large. Let's compare this to situations where we would certainly suspect
a clearer situation, like the aforementioned 30 out of 200 events,

{% highlight python %}
>>> dist = beta(30 + 0.5, 200 - 30 + 0.5)
>>> dist.mean()
0.15174129353233831
>>> dist.std()
0.025242965236046903
{% endhighlight %}

where we get a much narrower range of expected probabilities $\sim
0.15\pm 0.02$, and with "1 failures in 10", where a probability of
almost $0$, doesn't seem to be so far fetched:

{% highlight python %}
>>> dist = beta(1 + 0.5, 10 + 0.5)
>>> dist.mean()
0.125
>>> dist.std()
0.091724923213167844
{% endhighlight %}

# What is the Beta distribution?

The Beta distribution is a probability distribution, this means it is a
function, that we can use to obtain probabilities for "beta-distributed
values", expectancy values, variances and uncertainties. For us, the
most important properties are the mean $\mathcal{E}[x]$ and the variance
$\sigma^2$, whose square-root is the above standard deviation:

Mean:

$$\mathcal{E}[x] & = \frac{\alpha}{\alpha+\beta}$$

Variance $\sigma^2$:

$$
\text{Var}[x]  & = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha + \beta + 1)}
$$

The beta distribution is a distribution of a variable $x$, in our case
the failure rate / probability. Its parameters $\alpha$ and $\beta$ are
counts of binary situations/incidents, in our case the number of
successes and the number of failures. You can see that the mean of the
Beta-distribution is a formula for the very first failure rate we
calculated (when we were not using the Beta distribution). So I hope you
agree that it is a plausible candidate.

## How does this distribution look like?

We can easily visualize the distribution. With scipy, we can generate a
probability density function (pdf), and using matplotlib we plot this
function

{% highlight python %}
>>> x = np.linspace(0, 1, 1000)
>>> pdf = dist.pdf(x)
>>> plt.plot(x, pdf)
{% endhighlight %}

This gives us a plot of the probability density function

![What you see in this plot is the curve of the probability density
function of the Beta distribution. It's peak (in statistics lingo the
*mode*) is centered, near the mean of the distribution. We can see that
the distribution leans towards low values -- this underlines that from 3
failures vs 17 successful events, we see a tendency for the failure rate
to be rather at the low end.](/assets/images/distribution.png){: width="50%"}

From the spread of the distribution, we can infer that there is some
probability for very low failure rates, but also a probability for
failure rates above 40%!

To get a better feeling for the beta distribution, let's see how the
beta distribution behaves for a distribution with fewer events.

![Plot for $\text{Beta}\left(1 + \frac{1}{2}, 3 + \frac{1}{2}\right)$.
With fewer events, the distribution of the Beta-function is broader.
This shows how with fewer events the uncertainty is higher and the
distribution is not so closely localized around the
mean.](/assets/images/distribution_fewer_events.png){: width="50%"}

It is also more symmetric, because our summands of $\frac{1}{2}$ have a
greater influence, but more on this in the following section on priors.

## Why did I add one-half to each coefficient?

The summands of one-half that I added to each coefficient in the beta
distribution is a *prior*, more precisely a special prior, the
[Jeffreys' prior](https://www.wikiwand.com/en/Jeffreys_prior).

Just from looking at $\text{Beta}(a + \frac{1}{2}, b + \frac{1}{2})$ we
can see, that these prior terms kind of add two half-events to our
numbers of failures and successes. Thus, with such a prior, even without
counting any successes or failures, we already have a vague and broad
distribution for a failure rate. A prior encodes assumptions and
knowledge that we have **prior to** (before) recording data.

The Jeffreys prior is a *non-informative* prior, which means it has many
interesting properties, which don't interest us much today. I use this
prior here, so that the beta distribution does not blindly follow a few
data points. It regularizes the distribution slightly towards the center
and keeps it from getting narrow too soon, making the beta-distribution
a good choice even when looking at few observed events.

# Overview over the family of Beta-distributions

The following plot shows 25 Beta-distributions of the shape
$\text{Beta}\left(a + \frac{1}{2}, b + \frac{1}{2}\right)$. As you can
see, distributions add one failure event with each line downwards and
add one "success" event, with each column to the right.

So on the diagonal, you can see beta-distributions with equal number of
success and failure events, that are symmetric around 0.5. Their
distributions get smaller, the more events the distributions contain.

The success-only and failure-only beta distributions in the first line
and the leftmost column are very localized to the sides --- they do not
contain much conflicting information. Nevertheless due to the prior,
they still allow for the possibility the event-type not yet observed has
some probability.

![The vertical black lines are "quantiles" in steps of 1/20th of the
distribution. The closer the lines are, the denser the probability
distribution. The red line represents the
mean.](/assets/images/matrix.svg){: width="100%"}

# Incremental Updates: A Bayesian Approach

The approach I outlined above is a Bayesian one. Bayesian statistics is
a branch of statistics, that builds upon Bayes' theorem. Thanks to this
theorem and properties of the Beta-distribution, we can make use of a
very interesting property: Incremental updates. Let me explain this by
example.

Suppose we have not recorded any events yet, so we have no prior
knowledge about our system. We must assume a prior-distribution of our
failure rate that is non-informative: $\text{Beta}(x\mid\frac{1}{2},
\frac{1}{2})$. Now we observe $s$ successes and $f$ failures, and we
want to update the distribution with our new observations.

Bayes' theorem allows us to write down a so-called likelihood function.
In our case the binomial distribution is the perfect fit. Now the beauty
of this approach is, that for binomial likelihoods and beta-priors, we
receive a posterior distribution, that is a beta distribution with
slightly modified coefficients!

$$\text{Beta}\left(x \mid \frac{1}{2}+s, \frac{1}{2} + f\right) = \text{Binomial}\left(s, f\mid x \right) \text{Beta}\left(x\mid\frac{1}{2}, \frac{1}{2}\right)$$

If we make more observations, we can take the posterior as our new
prior, and repeat that pattern for every new data-point.

$$\text{Beta}\left(x \mid \frac{1}{2}+s+s', \frac{1}{2} + f + f'\right) = \text{Binomial}\left(s, f\mid x \right) \text{Beta}\left(x \mid \frac{1}{2}+s, \frac{1}{2} + f\right)$$

If we look at the Jeffreys prior from this perspective, we can think of
the $\text{Beta}\left(\frac{1}{2}, \frac{1}{2}\right)$
prior-distribution as an incremental observation of two half-events onto
those that we really observe. One of these half-events is a failure, the
other half-event is a success. Without observing any trial at all, these
"prior events" assume a failure-probability of 0.5 - a very neutral
starting point - which is spread out widely over the range from 0 to 1.

# Conclusion

When we use the beta-distribution, we indeed see, that "5 failures out
of 10 trials" is indeed a very different situation from "1 failure out
of 2 trials". We can use the Beta distribution in many situations with
binary outcomes. Using Bayesian priors, we can use the Beta-distribution
even with few events, avoiding overconfidence based on few observations.
