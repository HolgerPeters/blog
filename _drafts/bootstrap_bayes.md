---
layout: post
category: 'Data-Science'
date: '2016-12-08 21:30'
modified: '2016-12-08 21:30'
status: draft
tags:
 - data science
 - bayes
title: "Bayes'n'Bootstrap"
---

With the advent of machine learning into our IT landscapes,
a previously rather academic conflict of the statistical
community surfaces in blogs and other forums of discussion
every other week. It is the question of *frequentism* vs.
*Bayesianism*. This debate, often one that is as emotional
as the famous *editor-wars*, is in fact a very fundamental
one that touches the foundations of statistics and
probability theory. In that sense, it isn't your usual bike
shedding discussion, even if it is sometimes lead as one.
Metaphorically, it is a custody trial to determine who may
claim the interpretational sovereignty over nothing less
than the *Theory of Probability*.

frequentism and Bayesianism are both established approaches
to statistics. Their differences start, with their core
definitions. frequentism treats probabilities as ratios of
frequency-counts collected from an infinite number of
trials; and frequentist practitioners will tell you that a
finite number of trials will also suffice (as in: from 100
coin flips, 50 times we will obtain *head*, thus the
probability for head is $$\wp(H=1)=0.5$$).

For Bayesianists, probabilities are **degrees of belief**;
also Bayesianists use Bayes' theorem for inference.  A
Bayesianist would take the probability $$\wp(H=1)=0.5$$ in
the coin-flip example above to mean something like "It is
credible, that head and non-head (tail) are results of a
coin flip, without one option being more likely than the
other". A programmer can think of the Bayesian
interpretation of probabilities as an extension of Boolean
algebra: `true` (1, *firm-belief*) and `false` (0,
*firm-disbelief*)  are complemented with a spectrum of
values $$0 \ldots 1$$.

These brief characterizations are already enough to
understand much of the criticism either method faces:

* Bayesian probabilities are criticised as "subjective" or
  as not a genuine measurement parameter (degree of belief).
* frequentist probabilities are said to be limited to
  infinitely repeatable trials, and thus not applicable to
  any real world data set, with a finite number of
  measurements.

This criticism is too simplistic, however. And to those, who
strongly associate with one camp, there are probably many
embarassing commonalities: Both approaches often lead to
very similar results. In this post I will show you how you
can solve a problem with both methods and compare the
results.

# Estimating The Probability for a Bernoulli-Trial

We all expect coins to be fairly balanced. I.e. if we flip a
coin, we expect to roughly obtain head half of the times,
and tail the other half of the times. Yet there are many
processes with two outcomes, where we don't know the
individual probabilities beforehand. For example, a
researcher might be interested in the immunization rate of a
population.

Our researcher determines the immunization rate of $$N=40$$
people. The measured results could be  a series of numbers
(1 for immunized and 0 for not-immunized) like: `[1 1 1 1 1
1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 0 0 1 1 1 0 1 1 0 1 1
1 1 1 1 1]`.

The questions we are bound to solve are

 * What are the immunization rates (what is the probability
   for a person to be immunized)?
 * How reliable (and under what circumstances) would that
   inferred probability be?

# Frequentist Approaches

I divided this section into three parts

1. first we apply a common-sense approach to the problem
2. then, we see that our first approach is in fact the
   solution of the maximum-likelihood approach
3. we apply the bootstrap method to get more than just the
   maximum-likelihood estimate of the immunization rate.

## Common-sense (naïve) Treatment

A very simple approach to this problem is to just count the
number of immunized and the number of people screened. for
the above list, we have $$k = 34$$ immunized people of a
total of $$ N = 40 $$ people, which leads to an immunization
probability of $$0.85$$.

If the researcher had only screened the first 20 people, the
result would have looked a bit different, $$0.95$$. If we
had only looked at the probabilities from people 20-40, we
would have gottten a probability lower than $$0.85$$. Thus,
we have a method that gives us immunization rates, yet it
heavily depends on the sample size.  Also, we don't have a
means to quantify how certain we are about these enumbers.

## Maximum Likelihood Estimate

The likelihood-function [^likelihood]: $$L(\mu \mid N, k)$$
is the probability $$k$$ immunized subjects of $$N$$
subjects in total, under the condition of a parameter $$ \mu
$$, which we'll write down as $$ \wp(N, k \mid \mu) $$. We
identify, that his $$ \wp(N, k \mid \mu) $$ is the
[binomial distribution](https://www.wikiwand.com/en/Binomial_distribution).

$$
L(\mu) = \wp(N, k \mid \mu) = \text{Binomial}(k\mid N, \mu) = \binom N k  \mu^k(1-\mu)^{N-k}
$$

We now want to find the $$\mu$$ that maximizes the
likelihood $$L(\mu)$$. We could of course work out the
equations by hand. I use [sympy](www.sympy.org) here, which
will do all the tiresome calculations for us:

    In [1]: N, k, mu = symbols("N, k, mu")
    In [2]: likelihood = binomial(N, k) * mu**k * (1-mu)**(N-k)

Sympy will nicely render the likelihood term

    In [3]: likelihood
    Out[3]:
     k         N - k ⎛N⎞
    μ ⋅(-μ + 1)     ⋅⎜ ⎟
                     ⎝k⎠

Now let's see if sympy can come up with the derivative with
respect to $$ \mu $$:

    In [4]: diff(likelihood, mu)
    Out[4]:
       k         N - k ⎛N⎞    k                  N - k ⎛N⎞
    k⋅μ ⋅(-μ + 1)     ⋅⎜ ⎟   μ ⋅(-N + k)⋅(-μ + 1)     ⋅⎜ ⎟
                       ⎝k⎠                             ⎝k⎠
    ────────────────────── + ─────────────────────────────
              μ                          -μ + 1

Finally, we are only interested in the value of $$\mu$$,
for which the derivative is zero.

    In [5]: solve(diff(likelihood, mu), mu)
    Out[5]:
    ⎡k⎤
    ⎢─⎥
    ⎣N⎦

**Result:** We obtain $$\mu = \frac{k}{N}$$ as as the
maximum likelihood estimate, which basically is what we
expected as the naïve result.


## The Bootstrap Method

We can use the fact, that different subsets of our data
yield different results, to get a better picture of the
reliability / variance of our probabilities.

Just like above, we will take a look at subsets of the total
data set. However, this time we will take a systematic
approach. We will

* construct a new data sets from the recorded trials by
  randomized sampling with replacement. The new data set has
  the same size as the original one, but might contain some
  data points multiple times, and other data-points will be
  missing.
* calculate rates on the newly contructed data-set.
* Repeat this **many** times to get as many rates as
  possible (best: calculate it for all possible
  combinations, but mind the combinatorial explosion)
* plot the histogram of these rates (each subsample yielding
  one data point).

### Distribution of Rates in Subsample

The histogram below was made from a sample of 100
measurements, drawing many (100000) subsamples of 100
measurements, from which the rates were calculated.


{% highlight python %}
np.random.seed(1)
N = 100

x = scipy.stats.bernoulli(0.86).rvs(size=N)
m = np.fromiter((np.mean(np.random.choice(x, N))
                 for _ in range(100000)),
                dtype=float)

plt.hist(m, np.linspace(0, 1, 50))
plt.xlabel("Rate")
plt.ylabel("Occurences")
{% endhighlight %}


![histogram](/assets/images/histogram.png)

Depending on the subsample, we get different results for the
calculated rate. All calculated rates from a distribution.
We must assume, that the single rate calculated in the
maximum likelihood approach above is just as noisy as the
rates calculated in the bootstrap approach, because we
assume independence of the individual events. So the
bootstrapped rate distribution gives us an idea on how
credible and accurate the maximum-likelihood rate is.

# Bayesian Approach

**Note:** *If you aren't so much interested in Bayes'
theorem, you can just scroll down to the heading
"Incremental updates" and enjoy the graphs.*

## Bayes Theorem

Bayes' theorem is the central hub of Bayesian methods. It
is, however, not a postulated assumption, just happening to
work, but a direct consequence of *conditional
probabilities*. If you look at the probability for two
propositions[^prop] $$A$$ and $$B$$ &mdash; $$ \wp(A,
B)$$ &mdash; you can express this joint probability by
conditional probabilities:

$$
\wp(A, B) = \wp(A\mid B) \wp(B) = \wp(B \mid A) \wp (A)
$$

If we take $$A$$ for the probability of the street to be
wet, and $$B$$ for the probability of rainfall in the last
hour, then $$ \wp(A, B)$$ is the probabilty for *rainfall and
a wet street*. $$\wp(A\mid B)$$ is the conditional
probability for a wet street, **given** that it has rained,
$$\wp(B \mid A)$$ the conditional probability for rainfall,
given that the street is wet; and $$\wp(B)$$ is the
probability of rainfall, $$\wp(A)$$ is the probability of a
wet street.


We can rearrange the above equation dividing through $$
\wp(B)$$ on both sides and get an equation that expresses
the conditional probability $$\wp(A\mid B)$$ by the inverse
probability $$\wp(B\mid A)$$.

$$
\wp(A\mid B) = \frac{\wp(B \mid A)}{\wp(B)} \wp(A)
$$

Until now, *I think*, frequentists and Bayesianists can
agree. The disagreement starts on when and how to use this
equation. Bayesianists infer (conclude) $$ \wp(A\mid B) $$
on the left side of the equation from the right hand side.
Whereas critics of Bayesianism consider this to be a
dangerous endeavour.


### Bayes' Theorem and model estimation

Bayesian statistics is concerned with data $$D$$
and a model $$M$$ (a fit parameter, a parameter of a
distribution, a quantity that should be inferred). By
substituting $$A\to M, B \to D$$, we get Bayes' theorem with
Bayesian semantics:

$$
\wp(M\mid D) = \frac{\wp(D \mid M)}{\wp(D)} \wp(M)
$$

The probabilities involved are:

* $$\wp(M\mid D)$$ is the probability for the model, given
  data. Obtaining this probability distribution, we have the
  inference (Inference means nothing but: Estimating a model
  from/given data).

  We also call this quantity the *posterior*.
* $$\wp(D\mid M)$$ is the probability for data, given the
  model. This is the *likelihood* we have already seen above
  [^likelihood].
* $$\wp(M)$$ is the prior, a probability (distribution), that
  is independent of $$D$$.
* $$\wp(D)$$ is the probability for data[^evidence]. For this
  treatment here, we can think of it as a normalization
  constant (which can be very costly to compute).

The most important aspect of this theorem is: **We can
express the probability for a model, given data by some
term, that involves the probability for data, given the
model**.

Why is this important? Because it is often much easier to
give an expression for the, than to come up with the
posterior $$\wp(M\mid D)$$ directly.

## Bayesian Estimation of Immunization Rates

The immunization rate $$\mu$$ that we are looking for is a
probability (in the frequentist sense). Nevertheless, it is
in the Bayesian sense also model parameter $$ M = \mu $$,
whose probability distribution given data $$ \wp(\mu\mid
D)$$ can be inferred using Bayes' theorem.  We would like to
find the distribution for this parameter $$ \wp(\mu\mid D)
$$, so that we can get an expectancy value $$\mathcal{E}[\mu
\mid D]$$ and the variance.

Bayes rule gives us this distribution. First, we will ignore
the denominator, which is more of a normalization parameter,
without loss of generality, as

$$
\wp(\mu\mid D) \propto \wp(D \mid \mu) \wp(\mu).
$$

What could $$\wp(D\mid \mu)$$ be? During the trial, we have
$$k$$ observations of immunized subjects, out of $$N$$
observations in total, so $$\wp(D\mid \mu)= \wp(k \mid N,
\mu)$$. Does the k-out-of-N sound familiar?  It is what the
[Binomial distribution](http://en.wikipedia.org/wiki/Binomial distribution)
describes

$$
\wp(N, k \mid \mu) \sim \text{Binomial}(k\mid N, \mu).
$$

Now we need a suitable expression for $$\wp(\mu)$$. It needs
to be a probability distribution that just contains the
model alone (no data). This is a tough choice (and one of
the main sources for distrust of the Bayesian methods,
probably). Luckily, the Bayesian literature tells us, that
the Beta-distribution is a suitable choice for this,

$$
\wp(M) \sim \text{Beta}(\mu\mid \alpha_0, \beta_0)
$$

and $$\alpha_0$$ and $$\beta_0$$ are the *a priori*
parameters. Choosing $$\alpha_0=\beta_0=1$$ for example
would assume a uniform prior distribution between $$0 \leq
\mu \leq 1$$. I use $$\alpha_0=\beta_0=\frac{1}{2}$$
[^jeffrey].


### Incremental updates

Due to some neat properties of binomial and beta
distribution, what follows is that Bayes' theorem in this
instance simplifies to a very simple rule. Starting with a
Beta-prior distribution, we can obtain the posterior
distribution by just adding our observed $$k$$ and $$N-k$$
data points to the parameters of the beta distribution.

$$
\wp(\mu \mid N,k) = \text{Beta}(\mu\mid \alpha_0 + k, \beta_0 + (N-k))
$$

## Data

Using the above beta-prior model with our collected data, we
can obtain posterior distributions for the immunization
rate. The following plot shows such distributions, adding
more data with each subplot.

![distributions](/assets/images/distributions.png)

In the plot, we can follow along, how wit hmore data, the
distribution gets narrower (i.e. with more data, we are more
certain). The first subplot labelled $$ N= 0 $$ is the prior
distribution.

The infered value for the immunization rate, $$ \mu $$, is
the expectancy value of these distributions (represented by
the vertical black lines in the plot). For comparison, the
red, dotted line is the true immunization rate, that we
know, because we put it into the random number generator
that provides us with the data set.

We can see in the plots, that gradually our estimate
changes, as the data fluctuates, although with many
measurements it seems to stabilize. The learn curve is a
good way to visualize this.

# Learn curve for Bayes

Pretending that we only perform one trial at a time, we can
plot a learning curve that shows how our method performs and
how the inference quality improves with more data:

![learn curve for bayes](/assets/images/learncurvebayes.png)


# Learn curve for Boostrap

We have plotted a learning curve for the Bayesian approach,
how does the bootstrap method compare? Let's add a learn curve
for the bootstrap method to the plot:

![learn curve of both](/assets/images/learncurve-both.png)

What we can see here is, that with enough data points, both
methods give very similar results, to the point where they
seem equivalent.

However the Bayesian approach is better when infering from
fewer data points. Why is that?

* Bootstrap relies on constructing ad-hoc data-sets from the
  original samples. With few data points, it suffers from
  the same bias as the original sample.

  In our data set, the first few samples are `1`
  consistently, and thus the bootstrap approach must yield a
  rate of 1 and 0-sized error bars.

* The Bayesian approach uses a prior. This prevents the
  method from focussing too strongly on the first few
  events. Recording the first event, we do have error bars
  that are fairly large (which fits nicely with our
  expectation of being uncertain about the true value of our
  parameter).

The subtle, systematic difference that remains between the
Bayesian and the bootstrap method for larger sample sizes
(the Bayesian rate is consistently smaller than the
bootstrapped rate) is the influence of the prior, that never
completely vanishes (although it is negligible given the
statistical fluctuations).

# Conclusion

There are many conclusions that one can draw from this
simple example. Of course not everything that we can learn
from this example generalize to all questions about Bayes
and frequentism. So I'll limit my conclusion here to the
one very simple advice: I learned a lot more about
statistical methods and algorithms by constantly looking at
how Bayesianists and frequentists approach and derive them.
Most statistical topics are treated in Bayesian and
frequentist literature.

# Notes

Thank you Christopher and Daniel for your feedback on this
blog post.

## Further Reading

* [The Non-parametric Bootstrap as a Bayesian Model](http://www.sumsar.net/blog/2015/04/the-non-parametric-bootstrap-as-a-bayesian-model/)
  by Rasmus Bååth

## Footnotes

[^likelihood]:

    It is often said, that the likelihood isn't a
    probability (distribution), but another kind of function.
    This isn't correct. The likelihood is a probability
    (distribution).  What people mean when they say it isn't
    a probability is, that they don't use it as a
    probability (distribution) in that context, but as a
    function of some parameter, that is maximized (maximum
    likelihood estimation).

[^evidence]:
    It doesn't have a much of a canonical name. Calling it
    the *evidence* is popular. Since $$\wp(D) = \sum \wp(D
    \mid M_i) \wp(M_i)$$, I like "marginalized likelihood".

[^prop]:
    A proposition is a statement that can either be true or
    false.

[^jeffrey]:
    The prior distribution $$ \text{Beta}\left(\mu \mid
    \frac{1}{2}, \frac{1}{2}\right)$$ is called the
    [Jeffreys prior](https://www.wikiwand.com/en/Jeffreys_prior).
    Choice of priors would be the material for a series of
    blog posts.
