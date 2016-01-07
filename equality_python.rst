=================================================
Identical Objects Do Not Imply Equality In Python
=================================================

:date: 2016-01-07 20:41
:modified: 2016-01-07 21:16
:tags: python, interpreters, ruby
:category: python

Python has two very similar comparison operators: ``==`` for equality and
``is`` for object identity. Typically, ``is`` faster, as the implementation
just needs to compare object ids, whereas ``==`` must call the ``__eq__``
method, and is therefor slower.

The operator ``is`` is recommended for comparisons with ``None`` in Python (as
in ``if a is None``). And I was asking myself how much overhead the ``==``
method would be in this case. So I figured that the ``None == None`` case might
be more efficient, than the generic ``a == None`` case, because the runtime
could first check for identity before deciding to call ``__eq__``.

As it happens, Python has strange semantics with respect to these operators,
and my assumption was wrong. I was assuming that ``a == a`` was always ``True``
(since ``a is a`` is True, and identity should imply equality). This is,
however, not the case:

.. code-block:: python

   In [1]: class A:
      ...:     def __eq__(self, rhs):
      ...:         return False
      ...:

   In [2]: a = A()

   In [3]: a == a
   Out[3]: False

(tested with Python 3.5). [#f1]_

I haven't found much in the Python docs [#f2]_ about this, but I guess that
someone has a use case where ``a==a`` should evaluate to false, although
objects are identical. Another explanation would be that if ``__eq__`` would
have a side-effect, it should be called in any case, even for identical
objects. Right now, I cannot think of any cases where either of these options
would be desirable. So if you stumble over classes where ``a == a`` does not
evaluate to ``True`` it might be worth investigating.

Footnotes
---------


.. [#f1] Ruby does not do it any other way. I find it a bit less surprising,
         here, as we direcly overwrite the ``==`` operator that is called
         later, instead of Python's approach of using a protocol method
         ``__eq__``:

         .. code-block:: ruby

            irb(main):001:0> class A
            irb(main):002:1>     def ==(rhs)
            irb(main):003:2>         false
            irb(main):004:2>     end
            irb(main):005:1> end
            irb(main):011:0> a = A.new
            => #<A:0x007fda8190f2c8>
            irb(main):013:0> a == a
            => false
            irb(main):015:0> a === a
            => true

.. [#f2] https://docs.python.org/3/reference/datamodel.html?highlight=__eq__#object.__eq__
