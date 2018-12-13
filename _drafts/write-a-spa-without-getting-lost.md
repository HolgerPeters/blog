---
layout: post
category: Python
date: '2018-07-18 21:00'
modified : '2018-07-18 21:00'
status: draft
tags: 'Python, ember, api'
title: Writing SPA without getting lost
---

I never did many user interfaces. Surely, here and there did
I do some web sites, and commited changes to website
generators. But in general, I did more backend programming
or library / algorithmic / analytics code. Nevertheless, my
career did feature a short project where I had to build a
SPA (I was a junior dev and picked Clojurescript for the
task, I long left the company and hope no one had to pick
the code base up again. Points in my favour are, that
probably the codebase could still be rebuilt today which was
not common for Javascript code bases at the time. On the
other hand it might have been an exotic choice). Lately, I
have become interested again in writing user interfaces and
after some exploration I found a setup that is quite
workable for me -- a Python dev who isn't terribly firm in
the Javascript world. In this blog post, I will walk you
through building one of my favourite apps on my mobile phone
as a web service with a single page application frontend
(Wunderlist has been acquired and I fear that the service
will be terminated at some point in time).

For this we will use ember for frontend development and
flask for the backend.


# Getting Started

## Installing npm

For installing npm, follow the description on the npm
homepage. Homebrew users on the mac will just

    brew install npm

Then, install ember into the global namespace

    npm install -g ember-cli


## Putting up the project scaffold

Create an open folder and run

    ember init

This will install the ember javascript framework.
Should you get a warning about `destroy-app.js helper is not
present.`, you should be able to ignore it with a recent
`ember-cli` installation.

## How we proceed

We will start by first setting up the UI, only later will we
care about the backend. I work this way for a couple of
reasons:

* Ember has the tooling to do it, by offering the
  `mirage-cli` package that we can use to provide fake data
  while developing instead of using a proper backend.
* With my first attempts, started implementing a very rough backend
  first, then implementing the frontend, which left me in a
  situation where I had a backend service with many corners
  cut and buggy implementations that only ended up there
  because juggling frontend and backend development at the
  same time were confusing me. The cleanup was really
  exhausting.


## Data Models

Our application will need to deal with `users`, `tasks`, and
`lists`. Ember is opinionated about how data is represented.
So we will define an instance of ember's `Model` class for
each of these entities.


### Displaying users

First, we'll create a data model for users. A user is
typically represented by a user name, potentially an email
adress. With ember, we use the `ember` command on the
command line to generate the files for us before editing.

So after running `ember generate model user`, you should
find a file `app/models/user.js` and
`tests/unit/models/user-test.js` in your folder. In the user
model, we define all attributes and relationships of the
user, the attribute of the user is their username, and the
relationship is their lists.


    import DS from 'ember-data';

    export default DS.Model.extend({
      username: DS.attr('string'),
      lists: DS.hasMany('list'),
    });




We start with user
