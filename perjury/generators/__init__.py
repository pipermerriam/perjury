import random
import datetime
from decimal import Decimal
import itertools
import collections
from functools import partial

from perjury.content import (LAST_NAMES, FIRST_NAMES, WORD_LIST, USERNAMES)
from perjury.generators.datetime_generators import DatetimeGenerator

from perjury.generators.base import * # NOQA


class Generator(object):
    pass


# TODO: unique choice generator?  __unique__ magic method?
class Choice(Generator):
    """
    :class:`Choice` is a generator that is initialized with choices and will
    randomly return one of those choices when called.
    """

    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        return random.choice(self.choices)


def weighted_choice(choices):
    """
    :func:`weighted_choice` will take a dictionary of value goes to weight and
    will return a Choice generator for you. For example, if you defined and
    ``is_active`` generator like this::

        is_active = weighted_choice({
            True: 1,
            False: 3,
            })


    Statistically speaking, you would get 1 True for every 3 Falses.
    """
    counter = collections.Counter(choices)

    return Choice(choices=counter.elements())


# TODO: this is not a class, but it sort of acts like one.  Should it have a
# capital name?
def Repeat(value):
    return itertools.repeat(value).next


def smallint():
    return random.randint(1, 10)


def decimal():
    return Decimal(random.randrange(1000) / 100)


# TODO: timezone aware?
now = datetime.datetime.now
today = datetime.date.today
timenow = datetime.time

word = Choice(choices=WORD_LIST)


def words():
    return ' '.join(word() for i in range(smallint()))


first_name = Choice(choices=FIRST_NAMES)
last_name = Choice(choices=LAST_NAMES)
username = Choice(choices=USERNAMES)


def email():
    return '{0}@example.com'.format(username())


def url():
    return 'http://{0}.com'.format(username())


# How do we allow users to determine their own now function

class CurrentDatetimeGenerator(DatetimeGenerator):
    def end_at(self):
        return datetime.datetime.now() + datetime.timedelta(30)

    def start_at(self):
        return datetime.datetime.now() - datetime.timedelta(30)


current_datetime = CurrentDatetimeGenerator()
datetime_generator = DatetimeGenerator()


def sequence(start=1, incr=1):
    """
    Returns a Python generator that yields incrementing numbers forever.
    """
    while True:
        yield start
        start += incr


def consumer(iterable):
    """
    Takes a Python iterable and returns a perjury generator that
    will spit out an iteration every time called.
    """
    return partial(next, iter(iterable))
