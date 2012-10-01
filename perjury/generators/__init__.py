import random
import datetime
from decimal import Decimal
import itertools

from perjury.content import (LAST_NAMES, FIRST_NAMES, WORD_LIST, USERNAMES)


class Generator(object):
    pass


class Choice(Generator):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        return random.choice(self.choices)


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
