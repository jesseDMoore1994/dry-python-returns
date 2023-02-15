---
title: Meaningful return types and functional python with returns!
author: Jesse Moore
patat:
  eval:
    haskell:
      command: runghc
      fragment: true
    python:
      command: USERNAME=jmoore PASSWORD=nicetry python -
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

  As we navigate, I will attempt to showcase similar concepts as they appear
   in Haskell to try and highlight the inspiration. Although it is strictly
   not necessary for understanding *returns*, it may be interesting for the
   viewer.

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
    pure fuctions and providing tools to compose them in a (relatively) uncomplicated
    way.

---

# What are the tools returns provides to facilitate this? 

  *returns* provides two primary categories of __things__.

  There are __containers__ and then there are __compositional helpers__.

  - __containers__ are special boxes that are use to wrap values in a 
  computational context. (In Haskell, these types would be 
  considered instances of Monad.)

  - "Say the line Bart!" https://www.youtube.com/watch?v=NM3TU5VfEMM

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

---

# Result Container

Our next container is the result container, which can be used to convey
 either sucess or failure.

Lets say your application maintains a list of users as dictionaries, and
 you want to perform operations on that list.

```python
from returns.pipeline import flow
from typing import Callable, Iterable

my_users = [
    {"_id": "1", "first": "Jesse", "last": "Moore"},
    {"_id": "2", "first": "John", "last": "Doe"},
    {"_id": "3", "first": "Jane", "last": "Doe"},
]

def filter(users: Iterable[dict], key: str, value: str) -> Iterable[dict]:
    return [user for user in users if user[key] == value]

def get(users: Iterable[dict], key: str, value: str) -> dict:
    for user in users:
        if user[key] == value:
            return user
    raise RuntimeError(f"Cannot find a user with {key}: {value}!")

def filter_then_get(users: Iterable[dict], firstname: str, lastname: str) -> dict:
    return flow(
        (users, "last", lastname),
        lambda x: filter(*x),
        lambda y: get(y, "first", firstname),
    )

try:
    print(filter_then_get(my_users, "Jane", "Doe"))
    print(filter_then_get(my_users, "Midori", "Roman"))
except RuntimeError as ex:
    print(f"doh! {ex}")
```

---

# Result container 

In some scenarios, it may not be a bad thing that a user cannot be found,
 but it means that in those scenarios we need to write try except logic
 to catch the error. Instead, we could use *Result* to convey the failure
 explicitly without exceptions.

```python
from returns.pipeline import flow
from typing import Callable, Iterable
from returns.result import Result, Success, Failure
my_users = [
    {"_id": "1", "first": "Jesse", "last": "Moore"},
    {"_id": "2", "first": "John", "last": "Doe"},
    {"_id": "3", "first": "Jane", "last": "Doe"},
]

def filter(users: Iterable[dict], key: str, value: str) -> Iterable[dict]:
    res = []
    for user in users:
        if user[key] == value:
            res.append(user)
    return res

def get(users: Iterable[dict], key: str, value: str) -> Result[dict, str]:
    for user in users:
        if user[key] == value:
            return Success(user)
    return Failure(f"Cannot find a user with {key}: {value}!")

def filter_then_get(users: Iterable[dict], firstname: str, lastname: str) -> Result[dict, str]:
    return flow(
        (users, "last", lastname),
        lambda x: filter(*x),
        lambda y: get(y, "first", firstname),
    )

# works fine every time!
print(filter_then_get(my_users, "Jane", "Doe"))
print(filter_then_get(my_users, "Midori", "Roman"))
```

You can also use the __@safe__ decorator from the result module to convert
 a function that throws exceptions to one that returns failures with the
 exception that caused it. __@attempt__ will do the same except return the
 input that caused the exception rather than the exception itself.

---

# Result container 

Just like with the *Maybe* container, the *Result* container can be wrapped
around operations using the bind operator.

```python
from typing import Iterable
from returns.result import Result, Success, Failure, safe
my_users = [
    {"_id": "1", "first": "Jesse", "last": "Moore"},
    {"_id": "2", "first": "John", "last": "Doe"},
    {"_id": "3", "first": "Jane", "last": "Doe"},
]

@safe
def get(users: Iterable[dict], key: str, value: str) -> dict:
    for user in users:
        if user[key] == value:
            return user
    raise RuntimeError(f"Cannot find a user with {key}: {value}!")

# Can be used to provide context of the failure safely
print(get(my_users, "_id", "1").bind(safe(lambda x: x["first"])))
print(get(my_users, "_id", "4").bind(safe(lambda x: x["first"])))
print(get(my_users, "_id", "1").bind(safe(lambda x: x["middle"])))
```

---

# Haskell Either

```haskell
import Prelude hiding (last)

data User = User {_id :: String, first :: String, last :: String}

myUsers :: [User]
myUsers = [ User {_id = "1", first = "Jesse", last = "Moore"}
           , User {_id = "2", first = "John", last = "Doe"}
           , User {_id = "3", first = "Jane", last = "Doe"}
           ]

getUserByKeyValue :: [User] -> (User -> String) -> String -> Either String User
getUserByKeyValue users key value = if (length filtered_users) > 0 
                                    then Right $ head filtered_users
                                    else Left "Cannot Find User!"
    where 
    filtered_users = filter (\user -> key user == value) users

getValueFromUser :: (User -> String) -> User -> Either String String
getValueFromUser key user = Right $ key user

main = do
    print $ getValueFromUser first =<< getUserByKeyValue myUsers _id "1"
    print $ getValueFromUser first =<< getUserByKeyValue myUsers _id "4"
    -- Haskell won't allow you to try and access an invalid record field
    -- print $ getValueFromUser middle =<< getUserByKeyValue myUsers _id "4"
```

---

# Converters

Now that we have both *Maybe* and *Result*, it might be useful from time
 to time, to be able to go back and forth between the two types, you can
 do that using __converters__ *maybe\_to\_result* and *result\_to\_maybe*.

```python
from returns.converters import maybe_to_result, result_to_maybe
from returns.maybe import Some, Nothing
from returns.result import Success, Failure

print(result_to_maybe(Success(1)))
print(result_to_maybe(Failure(Exception)))
print(result_to_maybe(Success(None)))  # The docs say `Success(None)` this is supposed to be `Nothing`...
print(maybe_to_result(Some(1)))        # https://returns.readthedocs.io/en/latest/pages/converters.html#maybe-and-result
print(maybe_to_result(Nothing))
```

You can also use *flatten* to remove redundant layers of container.

```python
from returns.converters import flatten
from returns.maybe import Some, Nothing
from returns.result import Success, Failure

print(flatten(Success(Success(Failure(Exception)))))
print(flatten(Some(Some(Nothing))))
```

---

# IO Container

The next container is the *IO* container, we can use it to make our IO explicit.

Why do I want explicit IO? Consider we want to add the ability to read a life
 story from a file for a user. 

```python
from py.result import my_users, get, Result, Success, Failure
from returns.pipeline import flow
from returns.pointfree import bind
from typing import Iterable

def read_life_story(user: dict) -> Result[str, str]:
    life_story = f"life_stories/{user['first']}_{user['last']}"
    with open(life_story, encoding="utf-8") as f:
        return Success(f.read())

try:
    for _id in range(1, 5):
        print(
            flow(
                (my_users, "_id", f"{_id}"),
                lambda x: get(*x),
                bind(read_life_story)
            )
        )
except Exception as ex:
    print(f"doh! {ex}")
```

Uh oh, our code failed because we forgot to give Jane a life story! Worse yet,
 it blends into the code make hides the true complexity of the function which
 relies on the state of the filesystem!

---

# IO Container

Instead, we can use the *IO* container to highlight the IO side effects
 inherent to the function.

```python
from py.result import my_users, get
from returns.pipeline import flow
from returns.pointfree import bind
from returns.io import IOResultE, IOSuccess, IOFailure
from typing import Iterable


def read_life_story(user: dict) -> IOResultE[str]:
    life_story = f"life_stories/{user['first']}_{user['last']}"
    try:
        with open(life_story, encoding="utf-8") as f:
            return IOSuccess(f.read())
    except Exception as ex:
        return IOFailure(ex)

for _id in range(1, 5):
    print(
        flow(
            (my_users, "_id", f"{_id}"),
            lambda x: get(*x),
            bind(read_life_story)
        )
    )
```

---

# IO Container

You could also use the __impure\_safe__ decorator to wrap the function
 with IOResultE. Now we get the safety of the *IO* container and the
 readability of plain python.

```python
from py.result import my_users, get, Result, Success, Failure
from returns.pipeline import flow
from returns.pointfree import bind
from returns.io import impure_safe
from typing import Iterable

@impure_safe
def read_life_story(user: dict) -> str:
    life_story = f"life_stories/{user['first']}_{user['last']}"
    with open(life_story, encoding="utf-8") as f:
        return f.read()

for _id in range(1, 5):
    print(
        flow(
            (my_users, "_id", f"{_id}"),
            lambda x: get(*x),
            bind(read_life_story)
        )
    )
```

---

# Haskell IO

```haskell
import Prelude hiding (last)

data User = User {_id :: String, first :: String, last :: String}

myUsers :: [User]
myUsers = [ User {_id = "1", first = "Jesse", last = "Moore"}
           , User {_id = "2", first = "John", last = "Doe"}
           , User {_id = "3", first = "Jane", last = "Doe"}
           ]

getUserByKeyValue :: [User] -> (User -> String) -> String -> Either String User
getUserByKeyValue users key value = if (length filtered_users) > 0 
                                    then Right $ head filtered_users
                                    else Left "Cannot Find User!"
    where 
    filtered_users = filter (\user -> key user == value) users

getLifeStoryForUser :: User -> IO String
getLifeStoryForUser u = readFile filepath
    where
        filename = (first u) ++ "_" ++ (last u)
        filepath = "life_stories/" ++ filename

getLifeStory :: Either String User -> Either String (IO String)
getLifeStory = fmap getLifeStoryForUser

printLifeStory :: Either String User -> IO ()
printLifeStory user = do
    case getLifeStory user of
      (Left s) -> print s
      (Right y) -> y >>= print

main :: IO ()
main = do
    printLifeStory $ getUserByKeyValue myUsers _id "1"
    printLifeStory $ getUserByKeyValue myUsers _id "4"
    -- This line throws an error! how could we make it safe?
    -- printLifeStory $ getUserByKeyValue myUsers _id "3"
```

---

# Do Notation

There will be some scenarios where you want to use more than one container
 value. Since bind is with respect to only one container, it becomes a slog
 to pythonically write operations with multiple containers. Luckily, we can
 use __do notation__ to make this easier.

 ```python
 from returns.io import IO
 from returns.result import Result, Success, Failure

 print(
    IO.do(
        one + two
        for one in IO(1)
        for two in IO(2)
    )
)
 print(
    Result.do(
        good + bad
        for good in Success(1)
        for bad in Failure("crash")
    )
)
 ```

---

# Future Container

*Future* is useful in asynchronous applications, and serves to attempt and
 solve the following problems.
 

    1. You cannot call async function from a sync one

    2. Any unexpectedly thrown exception can ruin your whole event loop

    3. Ugly composition with lots of await statements


For example, you cannot call await coroutines in a synchronous context:
```python
def test():
    await my_async_routine()

print(test())
```

This function must instead be turned into an async function, then all
 caller functions must be, and so on. This makes composition between
 async functions and non async functions difficult. However, you can
 use return inside of async definitions to get awaitable values.

```python
import asyncio
async def test():
    return 1

print(asyncio.run(test()))
```

---

# Future Container

The *Future* container can then be used to compose these functions
 together, while maintaining a synchronous context at top level, only to
 allow a transformation to async when desired.

```python
import asyncio
from returns.future import Future

async def first() -> int:
    return 1

async def second(arg: int) -> int:
    return arg + 1

def main() -> Future[int]:  # sync function!
   return Future(first()).bind_awaitable(second)

print(first())
print(asyncio.run(first()))
print(second(first()))
print(asyncio.run(second(asyncio.run(first()))))
print(main())
print(asyncio.run(main().awaitable()))
```

---

# Haskell Async

Asynchronous processing requires much less syntactic sugar in Haskell.

```Haskell
import Control.Concurrent
import Control.Concurrent.Async

one :: IO Int
one = return 1

plusOne :: IO Int -> IO Int
plusOne x = do
    threadDelay 1000000
    fmap (+1) x

plusTwo :: IO Int -> IO Int
plusTwo x = do
    threadDelay 2000000
    fmap (+2) x

main :: IO ()
main = do
    res <- concurrently (plusOne one) (plusTwo one)
    print res
```

---

# Point free methods

There are times when using container methods are not fun. They aren't as easily
 composable when defining pipelines. I glanced over it earlier, when I was 
 discussing pipelines.

*pointfree* provides access to container functions like `.map` and `.bind`
 without requiring to call them on the container directly. In other words,
 it converts a function like "a -> Container[b]" to "Container[a] -> Container[b]". 
 This allows you to take what you would previously write `x.f(y)` and write it
 more like `f(x)(y)`.

```python
from py.maybe import get_root, divide
from returns.pointfree import bind
from returns.pipeline import flow, pipe

pointfree = flow(
    (4, 2),
    lambda args: divide(*args),
    bind(get_root),
)
print(f"{pointfree=}")

non_pointfree = flow(
    (4, 2),
    lambda args: divide(*args),
    lambda x: x.bind(get_root),
)
print(f"{non_pointfree=}")
```

---

# RequiresContext container 

The *RequiresContext* container allows you to rely on context from framework
 settings, environment, etc. without having to use side effects or passing 
 that information as a parameter.

For instance, have you ever needed to access a settings variable? You can
 can access them directly like this, but then your implementation is polluted
 with project specific details. 

 ```python
from py.config import SETTINGS

def sshpass_cmd(cmd: str) -> str:
    return (
        f"sshpass -p {SETTINGS['password']} "
        f"ssh -p {SETTINGS['port']} {SETTINGS['username']}@{SETTINGS['ip']} "
        f"{cmd}"
    )

def get_hostname() -> str:
    return sshpass_cmd("hostname")

print(get_hostname())
 ```

---

# RequiresContext container 

Without using returns, you could make the fuction pure again, but you would
 have to add settings as an argument up an and down the entire call stack.

 ```python
from py.config import SETTINGS

def sshpass_cmd(settings: dict, cmd: str) -> str:
    return (
        f"sshpass -p {settings['password']} "
        f"ssh -p {settings['port']} {settings['username']}@{settings['ip']} "
        f"{cmd}"
    )

def get_hostname(settings: dict) -> str:
    return sshpass_cmd(settings, "hostname")

print(get_hostname(SETTINGS))
 ```


---

# RequiresContext container 

With returns, you can write your functions in such a way that the dependency
 can be injected allowing us to more accurately acheive the single responsibility
 principle by programming against an interface rather than the dependency
 directly.

 ```python
from py.config import SETTINGS
from typing_extensions import Protocol
from returns.context import RequiresContext

class _Settings(Protocol):
    ip: str
    port: int
    user: str
    passwd: str

def sshpass_cmd(cmd: str) -> RequiresContext[str, _Settings]:
    def internal_sshpass_cmd(settings):
        return (
            f"sshpass -p {settings['password']} "
            f"ssh -p {settings['port']} {settings['username']}@{settings['ip']} "
            f"{cmd}"
        )
    return RequiresContext(internal_sshpass_cmd)

def get_hostname() -> RequiresContext[str, _Settings]:
    return sshpass_cmd("hostname")

print(get_hostname()(SETTINGS))
 ```

---

# Haskell "RequiresContext"

```Haskell
data Settings = 
    Settings {ip :: String, port :: Int, user :: String, passwd :: String}

class Monad m => SshContextM m where
  getSettings :: m Settings
  executeCmd :: String -> m String

mySettings :: SshContextM m => m Settings
mySettings = return $ Settings {ip = "1.1.1.1", port = 22, user = "test", passwd = "test"}

craftCmd :: Settings -> String -> String
craftCmd settings cmd =
    "sshpass -p " ++ passwd' ++ " ssh -p " ++ port' ++ " " ++ user' ++ "@" ++ ip' ++ " " ++ cmd
    where
     ip' = ip settings
     port' = show $ port settings
     user' = user settings
     passwd' = passwd settings

sshPassCmd :: SshContextM m => String -> m String
sshPassCmd cmd = getSettings >>= (\settings -> return $ craftCmd settings cmd)

instance SshContextM IO where
  getSettings = mySettings
  executeCmd = sshPassCmd

getHostname :: SshContextM m => m String
getHostname = executeCmd "hostname"

main :: IO ()
main = getHostname >>= print
```

---

# Closing Remarks

I think by now you get the point, I think I got the high level points. I didn't
 get everything though. Here are some points I didn't want to squeeze in.

 - You can create your own containers.
 - mypy/pytest integrations.
 - hypothesis integrations.
 - Foldables.
 - Currying. (partial is preferred by authors unless using integrations)
 - There is a whole library of helper functions, many I didn't cover.
 - works great with match expressions!

Many thanks to the dry-python team for returns, if they ever see this.

---

# Questions?
