Getting Started
===============

Getting up and running with Perjury generators is very simple.

.. codeblock::

>>> from perjury.generators import smallint
>>> smallint()
3
>>> smallint()
500
>>> [smallint() for x in range(10]
[48, 2, 71, 64, 3, 46, 99, 33, 80, 3]

Perjury is built around the concept of `callables`.  All generators provided by
Perjury implement the same simple interface.

**Calling the generator returns a value**

Admittedly :py:func:`perjury.generators.smallint` is not a very impressive
generator, so lets jump right into some real use cases.

.. highlight::

import random

usernames = ['animal', 'beaker', 'fozzie', ... , 'scooter']
def muppet():
    return random.choice(usernames)


When called, our function `muppet` will return a random name from our list of
usernames.
