================
Haskell by Types
================

:date: 2016-04-10 22:00
:tags: functional programming, haskell
:category: haskell

Getting a better understand of Haskell has always been on my
list. My typical toolbox for learning another programming
language is not so effective with Haskell, because in contrast to
say - Ruby [#f3]_  - learning Haskell requires me to learn new
concepts. On the other hand, Haskell offers some unique features
that actually make learning it surprisingly easy again.
One useful tool I like more and more about haskell is the
power of its type signatures. While learning Haskell you
cannot avoid to familiarize oneself with the type signatures.
But if you embrace them, it can boost your understanding
drastically.

The following compilation is of things I rather understood
recently, so bear that I might have missed one or the other
connection.

Overview
========

The purpose of this blog post is to explain some properties
of typical Haskell type classes by looking at the type
signatures of their member functions. So first of all, the
objective is to have these signatures ready for reading.
The following signatures were infered by looking for the type
signatures interactively in ghc's ghci prompt. One can also
`look into the source <https://hackage.haskell.org/package/base-4.8.2.0/docs/Control-Applicative.html>`_,
though, they should tell you the same.

Normal Functions
----------------

We'll start having a look at normal function applications.

.. code-block:: haskell

   ($) :: (a -> b) -> a -> b
   (.) :: (b -> c) -> (a -> b) -> a -> c


The `.` operator for function composition allows us
in Haskell to write ``(f . g) x`` instead of ``f (g x)``.

``$`` is a low-priority operator which represents the
function application, so instead of ``f x``, we can also
write ``f $ x``. It is mostly used to avoid parentheses in
code (to write ``f . g $ x`` for the above example), but
in this blog post, I will use it to represent
function application in general.

Functor
-------

In a FP, statically typed programming language without the
mathematical obsession of the haskell community, a functor
would rather be named "Mappable".

.. code-block:: haskell

   (<$>) :: Functor f => (a -> b) -> f a -> f b

There is also ``fmap``, which is just another name for ``(<$>)``.


Applicative
-----------

Applicative is a type class that represents sequential
computations, where a computation does not need a result
from its predecessor. Applicative values are also functors,
so you can use ``<$>`` with them.


.. code-block:: haskell

   pure  :: Applicative f =>          a -> f a
   (<*>) :: Applicative f => f (a -> b) -> f a -> f b -- sequential application
   (*>)  :: Applicative f =>        f a -> f b -> f b -- sequence action, discard the first value
   (<*)  :: Applicative f =>        f a -> f b -> f a -- sequence action, discard the second value

Monad
-----

Monads are characterized by the bind operator ``>>=`` and
the ``return`` operator. ``>>=`` passes a "monadic" value
``m a`` to a monadic function ``(a -> m b)``, ``return``
puts a value into a monadic container.

Monads are also Applicatives and Functors, i.e. they also
implement ``<$>``, ``<*>``, etc.

.. code-block:: haskell

   -- Sequentially compose two actions, passing any value produced
   -- by the first as an argument to the second
   (>>=)  :: Monad m =>        m a -> (a -> m b) -> m b        --
   (>>)   :: Monad m =>        m a ->        m b -> m b        -- discards value of first monad
   (<=<)  :: Monad m => (b -> m c) -> (a -> m b) -> (a -> m c) -- kleisli composition

   return :: Monad m =>      a -> m a
   fail   :: Monad m => String -> m a


Functions that apply functions
==============================

The ``<*>`` operation of the Applicative (sequential
application) and the function application operator ``$``
have a pretty similar signature:

.. code-block:: haskell

   ($)   ::                    (a -> b) ->   a ->   b
   (<$>) :: Functor f     =>   (a -> b) -> f a -> f b
   (<*>) :: Applicative f => f (a -> b) -> f a -> f b

The first operand of those operators are functions, mapping
from one type ``a`` to the other ``b`` (in the case of
``<*>`` it's a function in an applicative of such a function).
The second operand is the argument to the application. In
the case of normal function application this is plainly the
function argument, with the Functor ("Mappable") it is a
functor, in the case of the applicative it is an applicative.
The result of the operation is either of type ``b``, functor
of ``b`` or applicative of ``b``.

One instance of Functor and Applicative  (a Functor is
always an Applicative) is the list ``[]`` type.
The following ghci interactive session will demonstrate
the three applying operators:

.. code-block:: haskell

   > (+10) $ 1
   11
   > (+10) <$> [1,2,3]
   [11,12,13]
   > (+) <$> [1,2,3] <*> [10, 20, 30]
   [11,21,31,12,22,32,13,23,33]

Let's investigate the type properties of that last statement
(which mapped the addition on a list of integers and seq.
applied it to another applicative, a list):

.. code-block:: haskell

   > let mapAndApply x y z = x <$> y <*> z
   > : mapAndApply
   mapAndApply :: Applicative f => (a1 -> a -> b) -> f a1 -> f a -> f b

Thus, Haskell infers types for ``x :: (a1 -> a -> b)``, for
the second argument ``y :: f a1`` and ``z :: f b``.
This combination is a common function, called ``liftA2``

.. code-block:: haskell

   liftA2 :: Applicative f => (a -> b -> c) -> f a -> f b -> f c

We can read ``liftA2 (+)`` as "lift the addition to an
applicative action". After lifting, he have an addition for
all applicatives.

.. code-block:: haskell

   > let addApplicative = (liftA2 (+))
   addApplicative :: (Num c, Applicative f) => f c -> f c -> f c

To prove the point, we can experiment with this using
various applicatives in the Haskell's std. library

.. code-block:: haskell

   > addApplicative (Just 1) Nothing
   Nothing
   > addApplicative (Just 1) (Just 2)
   Just 3
   > addApplicative Nothing (Just 2)
   Nothing
   > addApplicative Nothing Nothing
   Nothing
   > addApplicative Nothing Nothing
   Nothing
   > addApplicative (Right 5) (Right 6)
   Right 11
   > addApplicative (Right 5) (Left "a")
   Left "a"
   > addApplicative [1,2,3] [10,20,30]
   [11,21,31,12,22,32,13,23,33]
   > addApplicative [1,2,3] []
   []

The same evaluations can also be written in applicative
style.

.. code-block:: haskell

   > (+) <$> Just 1 <*> Nothing
   Nothing
   > (+) <$> Just 1 <*> Just 2
   Just 3
   > (+) <$> Nothing <*> Just 2
   Nothing
   > (+) <$> Nothing <*> Nothing
   Nothing

Example: Generating a stream of unique labels
---------------------------------------------

This will be a "more real-world" example that uses ``liftA2``
or ``<$>`` and ``<*>``. Suppose we need to generate labels in
code, for example while performing operations on an abstract
syntax tree. Each label needs to be unique, and we need labels
in various functions. Since we use Haskell and pure-functions,
we cannot just mutate some counter-variable.

.. code-block:: haskell

   import Control.Monad.State
   import Control.Applicative

   type LabelM = State Int

   increment :: LabelM String
   increment = state $ \i -> let j = i + 1
                             in ("$" ++ show j, j)

   labels :: Bool -> LabelM [(String, String)]
   labels discard = f <$> twoLabels
                      <*> twoLabels
                      <*> twoLabels
                  where f a b c = if discard
                                  then [a, c]
                                  else [a, b, c]
                  -- (,) <- is an operator creating a tuple
                  twoLabels :: LabelM (String, String)
                  twoLabels = (,) <$> increment <*> increment

   main :: IO ()
   main = do putStrLn "Enter `True`, or `False`"
             discard <- getLine
             print (evalState (labels . read $ discard) 0)

When executed, this program will prompt you to enter either
``True`` or ``False``, and then it will print out results,
depending on the input. Either ``[("$1","$2"), ("$5","$6")]``
or ``[("$1","$2"),("$3","$4"),("$5","$6")]``. Notice how even
if the second label-pair is discarded after all, the counter
is still incremented. The entry point is the evaluation of
``evalState`` in ``main``. Here, we initialize the state
monad's state with 0 and evaluate the monadic ``test``
function. The state is managed by the state monad
``LabelM = State Int``, which directly tells us
that our state consists of an integer variable.
Finally we have ``increment``, which increments, that internal
state and returns a label, as well as ``twoLabels``, which
generates a pair of such labels (by lifting ``increment``).
Note that both ``increment`` and ``twoLabels`` are of type
``LabelM _``, once ``LabelM String`` and ``LabelM (String,
String)``.

We use ``twoLabels`` in the ``labels`` function, where we
use applicative style to obtain the unique labels and either
return them all, or throw away some [#f4]_. I condensed this
use case from abstract syntax tree (AST) rewriting code, and
if it wouldn't blow up the example code, I would show code
here, that introduced labels depending on the AST input to
the program.

Solving this issue with label has some benfits. First of
all, it makes the state explicit in the type signatures,
which gives you the guarantee that if you are not using the
``LabelM`` type, you are not touching that state.
Then, the state is handled just like any other value in
Haskell -- immutable. ``evalState`` is the bottleneck (in a
good sense), that allows us to evaluate our "stateful" code
and fetch it over in the LabelM-free world.


Composition Patterns
====================

Another interesting pair of operations with a similar
signature are the operators ``(.)`` and ``(<=<)``.

.. code-block:: haskell

   (.)   ::            (b ->   c) -> (a ->   b) -> (a -> c)
   (<=<) :: Monad m => (b -> m c) -> (a -> m b) -> (a -> m c)

The correspondence here is between functions of type ``(b -> c)``
and monadic functions of signature ``Monad m => (b -> m c)``. I.e.
the signatures of ``(.)`` and ``(<=<)`` have almost the same
pattern.

We know this ``Monad m => (b -> m c)`` signatures from the
bind-operator's second operand:

.. code-block:: haskell

   (>>=) :: Monad m => m a -> (a -> m b) -> m b

By joining two ``M a >>= \x -> M b`` operations, I aim to
infer  ``(<=<)``, we'll use the ``Maybe`` monad and I'll
write the signatures of the lambda functions to the right.

.. code-block:: haskell

   printLengthPrint :: Int -> Maybe Double
   printLengthPrint = \w -> Just (show w)    -- :: Int -> Maybe String
                  >>= \x -> Just (length x)  -- :: String -> Maybe Int
                  >>= \y -> Just (2.0 ^^ y)  -- :: Int -> Maybe Double

We can kind of identify the signature of ``(<=<)`` just by
looking at this. Now spell out the lambda functions in
point-free style (I called them ``f,g,h``) and we can
implement the ``printLengthPrint`` function by Kleiski's
composition

.. code-block:: haskell

   f :: Int -> Maybe String
   f = Just . show
   g :: String -> Maybe Int
   g = Just . length
   h :: Int -> Maybe Double
   h = Just . (2.0 ^^)

   plp1 = h <=< g <=< f
   plp2 = f >=> g >=> h

To sum it up: Functional programming is often defined as
programming by function composition and application. Monads
are a functional concepts, and we can see that monads compose
in a strikingly similar way. I think this underlines that
Monads are indeed a functional concept (and not -- like
sometimes stated -- imperative programming in sheep's
clothing).

Resources
=========

For more detail on Haskell's types see the
`Typeclassopedia <https://wiki.haskell.org/Typeclassopedia>`_.

To familiarize yourself with Functors and Applicatives, it
is really great to write parsers with `megaparsec
<https://mrkkrp.github.io/megaparsec/>`_.

`What I wish I knew <http://dev.stephendiehl.com/hask/>`_ by
Stephen Diehl is also a great source.

Footnotes
=========


.. [#f1] type signatures can be obtained by running ghci and asking it for types

   .. code-block:: haskell

        Prelude> import Control.Monad
        > :t (>>=)
        (>>=) :: Monad m => m a -> (a -> m b) -> m b
        > :t (>>)
        (>>) :: Monad m => m a -> m b -> m b
        > :t return
        return :: Monad m => a -> m a
        > :t fail
        fail :: Monad m => String -> m a
        > :t (<$>)
        (<$>) :: Functor f => (a -> b) -> f a -> f b
        > :t (<$)
        (<$) :: Functor f => a -> f b -> f a
        > :t pure
        pure :: Applicative f => a -> f a
        > :t (<*>)
        (<*>) :: Applicative f => f (a -> b) -> f a -> f b
        > :t (*>)
        (*>) :: Applicative f => f a -> f b -> f b
        > :t (<*)
        (<*) :: Applicative f => f a -> f b -> f a
        > :t ($)
        ($) :: (a -> b) -> a -> b
        > :t fmap
        fmap :: Functor f => (a -> b) -> f a -> f b
        > :t (<=<)
        (<=<) :: Monad m => (b -> m c) -> (a -> m b) -> a -> m c
        > :t (.)
        (.) :: (b -> c) -> (a -> b) -> a -> c

.. [#f2] Some notes on Tooling

   In my experience, I learned the best with Haskell,
   when I used appropriate tooling. They accelerate
   learning Haskell so much.

   `hlint
   <https://hackage.haskell.org/package/hlint>`_ is
   your friend with invaluable information. It
   notifies you when you use redundant brackets and
   this feedback will familiarize you with operator
   precedence much quicker. Like any linter, I suppose that
   hlint's value is probably at its peak when used by
   beginners and  I expect it will be less valuable to me
   over time. Nevertheless I don't want to go without it
   right now.

   I use neovim with the plugins ::

           Plug 'benekastah/neomake'
           Plug 'dag/vim2hs'
           Plug 'bitc/vim-hdevtools'


   Pointfree is another tool, that I use (curiously), it
   transforms your code to point-free style. I often use it
   when I feel that a line of code could possibly be written
   in point free style, check it out and revert back if I
   feel normal-style Haskell is better. This has taught me
   some things I probably wouldn't have discovered for a
   long time, for example that ``(,)`` and ``(+3)`` exist,
   etc.

.. [#f3] A Python programmer will probably pick up Ruby's
   language features rather quickly and huge portions
   of the time learning Ruby will be spent on
   familiarizing onesself with the standard library.

.. [#f4] My first intuition here was to use monadic
   functionality  (``>>=``), yet as it turns out,
   functor and applicative (``<*>``) is enough. This
   confused me: If applicatives were about sequential
   actions, where the current item does not know about its
   predecessor, how could it increment the state-monads
   state? The answer is in the signatures:

   .. code-block:: haskell

           (<*>) :: Applicative f => f (a -> b) -> f a -> f b

   The ``f (a -> b)`` piece tells us, that we map from one
   value of the applicative to another. the consecutive ``->
   f a -> f b`` tell us, that our ``(a -> b)`` operation is
   applied to ``f a`` to yield ``f b``. Thus shouldn't have
   surprised me that applicative is in fact capable of
   incrementing the counter.

   For comparison, Monad's bind also  has this mapping from
   ``a`` to ``b`` in it's signature, however in the form of
   ``(a -> m b)``.

   .. code-block:: haskell

      (>>=)  :: Monad m =>        m a -> (a -> m b) -> m b

.. vim:tw=60:
