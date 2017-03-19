---
layout: post
category: Python
date: '2017-03-19 12:05'
modified: '2017-03-19 12:05'
tags: 'practice, agile, engineering'
title: Work Around the Workarounds
---

In their worst incarnation, workarounds can put development
and migrations of software projects to a grinding halt. Their _ad hoc_
nature — they are rarely a long-term plan — and their
tendency to span across abstraction layers and to depend on
circumstances make them a tough issue in the long run. So just why do we
introduce them in the first place?

Workarounds often start with two things: a goal and a
problem. A goal that we want to achieve, and a problem, that
is deemed either unfixable or too costly/difficult to fix.
The plan is then, to work around the obstacle instead of
solving a root cause of the issue.

### Software Workarounds Are Hard To Keep In Check

_The workaround is the software-equivalent to using a
bucket under a leaky roof. The difference in software is,
that it is sometimes hard to see when a workaround has
reached the complexity of the fix. You wouldn't install a
sewer-pipe to that bucket, would you?_

At the heart of the decision to introduce a workaround are
estimates (either formal or informal ones). Estimates for the effort needed to do a fix of
the root cause, and an estimate for the effort needed to
work around this issue. Even if it isn't a conscious
estimate, the implementation of a workaround means that
we think, the root-cause-fix is more costly than the
workaround. This is especially tempting within a
time-constraint. A deadline, a merge-window closing, or our
urge to complete the implementation of a feature are all
incentives for us to work around.

## The Interest Rate

However, again and again I have observed situations like the
following: _The codebase needs to migrated to run on a newer
system. As a consequence, I need to do some adjustments
to reflect API changes. This is when I stumble over some
awkward code, that needs to be changed as well. I
realise test coverage for these functions isn't great, and I finally see: This is a workaround, at least it used to be. It
takes me about half an hour to fix the actual problem and I can
delete the workaround code without porting it (which takes me another half an hour until I cleared up the remnants). I ask
myself: How much effort has been spent before, when
migrating workaround code once already seems more
difficult than fixing the problem worked-around?_

The realisation: Work arounds are a mortgage. They may ease
your life for the moment, but in the end you need to pay
back with interest.

So, when we often opt for the workaround, and underestimate
its costs, why is this?  It is, because we don't make an
estimate for the *interest rate* that we will have to pay for
the workaround. It is the fixation on a single goal, the
deadline, the closing of a ticket, deploying a new version
of the software, or getting it to run in some other
configuration. We make them our primary goals and any means
are just right to achieve them.

### Comfort Zones

Another important factor is comfort. Workarounds happen in
our artefacts, in our comfort zone, when the root cause is
often in an *upstream* package, an (hopefully open source)
software or parts of the code base we just don't know so
well. So when there is a bug in a dependency of ours, we are
much more likely to work around it, than to submit a PR with
a fix. 


Even more astonishing is the observation, that many
of such workarounds are not even accompanied with bug
report in the upstream package's issue tracker, which is the
lowest effort I can think of to get an upstream issue fixed.


## Avoiding the Workaround

Surely, not every workaround can be avoided, so my goal is,
to not introduce them lightheartedly, but also be reasonable
when they are needed. A checklist might help here:

* Has the (root) cause of our problem been triaged and
  identified? _More often than not are we acting on rough
  assumptions or loose correlations._

* Have experts been consulted (colleagues, StackOverflow,
  supporting consultants, IRC, ...) _If workarounds are
  endorsed by third-parties it might be a hint that a
  workaround is indeed the best resolution for now._

Don't start to implement a workaround over an upstream issue
without having reported the problem upstream (bug ticket
filed/opened) or having verified that someone else has
reported this as an issue.

*Has the option to fix the root cause been discussed?* Too
often, it is not considered at all as an option to fix the
root cause of a problem. So make sure you actually talk
about this as an option.


## Embracing The Workaround

There are tons of reasons why, even after fixing the root
cause upstream, a workaround might still be necessary.
Classic example: OSS release cycles are longer than your
sprint. Or the project is not responsive to your pull
request. In such cases we don't have a choice and need to implement a temporary workaround. Then, we definitely need to make sure, that when we
implement the workaround, it is marked as such in code and
communicated accordingly. If a new colleague arrives, they
shouldn't have to assume that "it seems this is the way XYZ
is done here", but they should be able to see, that this
patch of code is a workaround that can hopefully be removed
already, or in the foreseeable future.
