---
layout: post
category: Python
date: '2018-11-23 22:05'
modified: '2018-11-22 22:05'
tags: 'practice, agile, engineering'
title: 'Trunk Based Development'
---

Have you or a colleague ever spent a whole day trying to
merge a feature branch into your master branch, and you
couldn't finish that merge (or you event started the merge
from scratch the next day hoping that you had messed
something up and wouldn't repeat that a second time)?

Have you ever realized that in your team's Github/Atlassian
Stash / Gitlab repository, pull requests and branches pile
up without getting merged?

I am sure you have, and then you have witnessed a problem
with your integration and software development workflow.
Integration and merging has always been a tricky business in
software development, so they are not new. In waterfall
software development in the 80ies, integration phases could
go for months. So surely, development practices and tooling
has considerably improved since then.

However, I feel a resurgence of merge and integration
problems and it has only getting stronger over the years.


# Branching

Branching by itself is a problem we typically cannot avoid
when several people work with text[^no-branching].
Basically the problem of branching arises, if two people
edit a document (or in the case of source code, a source
tree) at the same time. Starting from the same snapshot,
if person A and person B make changes, they will create two
conflicting versions of the source.

If you represent the history of the document as a graph, you
would have to represent two people editing the source as a
bifurcation, a branch.

When you check out repository from github to your local
machine and make changes there, you in fact have started to
_branch_ off the remote repository, even though you didn't
explicitly create a _git branch_.

The Problem with branching arises, when person A and person
B want to combine their changes, into a new, joint revision
of the source code.



# Feature Branch Workflows



# Trunk Based Development
# Feature Branches Revisited
# Are you really sugesting...?

There is no legal mandate for feature branches.

[^no-branching]:
   Actually, there are ways to avoid it. One would be to use
   a multi-user editor, that shares a common memory section
   for documents and allows for collaborative editing. For
   programming, I assume this would cause all kidns of other
   problems when people edit the same repository checkout at
   the same time.
   The other is to take turns at editing code. Early version
   control systems (VCS) allowed for users to lock files,
   which in principle is a way to avoid having to merge two
   edits.
