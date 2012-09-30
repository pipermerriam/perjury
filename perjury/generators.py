import random
import datetime

from perjury.content import (LAST_NAMES, FIRST_NAMES, WORD_LIST, USERNAMES)


class Generator(object):
    pass


class Choice(Generator):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        return random.choice(self.choices)


def smallint():
    return random.randint(1, 10)


# TODO: timezone aware?
now = datetime.datetime.now

word = Choice(choices=WORD_LIST)


def words():
    return ' '.join(word() for i in range(smallint()))


first_name = Choice(choices=FIRST_NAMES)
last_name = Choice(choices=LAST_NAMES)
username = Choice(choices=USERNAMES)


def email():
    return '{0}@example.com'.format(username())
