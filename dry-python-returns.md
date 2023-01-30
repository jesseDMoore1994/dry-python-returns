---
title: Meaningful return types and functional python with returns!
author: Jesse Moore
patat:
  eval:
    haskell:
      command: runghc
      fragment: true
    python:
      command: python -
      fragment: true
...

---

# HuntFunc Plug

  Before getting started... Are you interested in functional programming?
  Do you live in the hunsville area? If so, consider joining HuntFunc!

  - Google group: https://groups.google.com/u/1/g/huntfunc

  - twitter: https://twitter.com/huntfunc

  - website: http://huntfunc.github.io/

---

# Let's Get Started!

  The presentation today is: *Meaningful return types and functional python with returns!*

  This presentation will serve to shortly explain:

  - What is the problem *returns* is trying to solve?

  - How does *returns* contribute to solving those problems?

  - How can *returns* help you program pythonically in a functional style?

  As we navigate, I will attempt to showcase similar concepts as they appear Haskell.

---

# The pitch

  Why should you use *returns* when developing python projects? There are a ton
   of features dry-python's return boasts, available on the github page.

  I will elect to just describe what I personally find useful about it. In general
   I would say that *returns*...

  - ... tends to make my python code more expressive instead of obfuscating my
    programmatic intent.

  - ... forces me to examine and be concerned with the edge cases of my software
    by forcing safe types on me instead of muttling them around the boundary of
    control flow.

  - ... guides me to separate architectural concerns by making it easier to write
    pure fuctions and providing tools to compose then in a (relatively) uncomplicated
    way.

---

# What are the tools returns provides to facilitate this? 

  *returns* provides two primary categories of __things__.

  There are __containers__ and then there are __compositional helpers__.

  - __containers__ are special boxes that are use to wrap values in a 
  computational context. (In Haskell, these types would be 
  considered instances of Monad.)

    ヽ(;ﾟ;∀;ﾟ; )ﾉ --- Oh no, he said Monad! Panic!

    (=￣▽￣=)Ｖ --- do not worry, last time I'm mentioning it, no need to go
                learn category theory just yet!

  - __compositional helpers__ are tools that can be used to make first
  class function use with our containers more pythonic and remove some
  of the manual drudgery of working directly with the containers.

---

# Simple example to start!

  Lets take a look at our first container. The *Maybe* container.

```python
from math import sqrt
from typing import Optional
from returns.maybe import Maybe, maybe

@maybe
def get_root(square: float) -> Optional[float]:
    if square >= 0:
        return sqrt(square)

print(get_root(4))
print(get_root(-4))
```

What is happening here? We are actually using the *maybe* decorator to
 wrap the return of our function in the *Maybe* container. 

---

# Maybe container

 We could also elect to do this directly, rather than using the decorator, 
 like so.

```python
from math import sqrt
from returns.maybe import Maybe, Some, Nothing

def get_root(square: float) -> Maybe[float]:
    if square >= 0:
        return Some(sqrt(square))
    return Nothing

print(get_root(4))
print(get_root(-4))
```

Why would we want to do this? For one simple reason, it gets rid of the
 *None* value. Beyond being the "billion dollar mistake" which nullables
 have grown to be described, handling them introduces a complexity overhead
 that destroys readability.

---

# Maybe container

We can use these containers to chain multiple operations together and 
 eliminate the *None* checks!

 With returns! :)
```python
from math import sqrt
from typing import Optional
from returns.maybe import Maybe, maybe

@maybe
def get_root(square: float) -> Optional[float]:
    if square >= 0:
        return sqrt(square)

@maybe
def divide(numerator: float, denominator: float) -> Optional[float]: 
    if denominator != 0:
        return (numerator/denominator)

print(divide(4, 2).bind(get_root))
print(divide(-4, 2).bind(get_root))
```

---

# Maybe container

without returns... :(
```python
from math import sqrt
from typing import Optional

def get_root(square: Optional[float]) -> Optional[float]:
    if square is not None:
        if square >= 0:
            return sqrt(square)

def divide(numerator: float, denominator: float) -> Optional[float]: 
    if denominator != 0:
        return (numerator/denominator)

print(get_root(divide(4, 2)))
print(get_root(divide(-4, 2)))
```

These None checks would only spiral further and every function written that
 would receive a *None* would have to validate it. Using returns, we can write
 code without fear of the *None* case and trust the bindings.

---

# Haskell Maybe

Haskell has a Maybe type that seems inspirational. (This is a recurring theme)

```haskell
import qualified Prelude
import Prelude hiding (sqrt, div)

sqrt :: Float -> Maybe Float
sqrt x
    | x < 0     = Nothing
    | otherwise = Just $ Prelude.sqrt x

div :: Float -> Float -> Maybe Float
div x y
    | y /= 0    = Just $ (/) x y
    | otherwise = Nothing

main = do
    print $ sqrt =<< div 4.0 2.0
    print $ sqrt =<< div (-4.0) 2.0
```


(Notice the `=<<` operator, this is haskell's bind function, which does
 the same thing as `.bind` in the statement `divide(4, 2).bind(get_root)`.

---

# Pipelines (pipes and flows)

Lets take a quick interlude to talk about our first __compositional helper__.

It is quite common in a functional style to want to compose functions together.
 __Pipes__ and __flows__ can help to define a data pipeline with your 
 functions. The only distinction being that __flows__ are used when you have 
 something to act on immediately, and __pipes__ can be used to hold a
 composition until it can be used later.

```python
from py.maybe import get_root, divide
from returns.pointfree import bind
from returns.pipeline import flow, pipe

f = flow(
    (4, 2),
    lambda args: divide(*args), #Here I am widening args for python
    bind(get_root),
)
print(f"flow: {f}")

divide_then_root = pipe(
    lambda args: divide(*args),
    bind(get_root),
)

print(f"pipe: {divide_then_root((4,2),)}")
```

