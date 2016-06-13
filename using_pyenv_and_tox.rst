===================
Using pyenv and tox
===================

:date: 2016-05-14 17:26
:modified: 2016-05-14 17:25
:tags: Python, tox, pytest
:category: python


I usually use `pyenv <https://github.com/yyuu/pyenv>`_ to manage my Python
interpreters and obtain them in whatever version I need. Another tool I
occasionally use is `tox <tox.readthedocs.io>`_ by Holger Krekel, which nicely
generates build matrices for library and python interpreter versions, that come
handy when you develop a library targeting multiple Python versions (and
dependencies).

However, until recently I didn't know how to use the two of them together.
With ``pyenv``, I  usually ended up with one python interpreter in my path, so
tox had only one interpreter to choose from, and I was missing out on tox'
selling point: testing your code over various versions of Python.

Install Multiple Python Version With Pyenv
==========================================

Setting up your pyenv usually looks like this::

     % pyenv install 3.5.1
     % pyenv install 2.7.10
     % cd my_project_dir
     % pyenv local 3.5.1

Now it is possible to use multiple Python versions here::

    % pyenv local 3.5.1 2.7.10
    % python3.5 --version
    Python 3.5.1
    % python2.7 --version
    Python 2.7.10

Then, tox can find interpreters, typically you will have a ``tox.ini`` in your
project that starts with something like this:

.. code-block:: ini

   [tox]
   envlist = py27,py34,py35
   skip_missing_interpreters = True

   [testenv]
   commands=py.test
   deps = -rrequirements.txt

Invoking ``tox`` should now run tox with the two available Python versions, 2.7
and 3.5, skipping 3.4 unless it is installed.
