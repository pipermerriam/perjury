"""
Future plans

1. Ability to randomize a generators return values.
2. Enforce Uniqueness across results.
"""
import random

from pyrite.base import (BaseGenerator, WordGenerator, MultiGenerator,
        RepeatValueGenerator)
from pyrite.content import (MALE_NAMES, FEMALE_NAMES, LAST_NAMES, FIRST_NAMES,
        WORD_LIST, USERNAMES)


class NameGenerator(WordGenerator):
    words = FIRST_NAMES


class MaleNameGenerator(WordGenerator):
    words = MALE_NAMES


class FemaleNameGenerator(WordGenerator):
    words = FEMALE_NAMES


class LastNameGenerator(WordGenerator):
    words = LAST_NAMES


class UsernameGenerator(WordGenerator):
    words = USERNAMES


class FullNameGenerator(BaseGenerator):
    first_names = FIRST_NAMES
    last_names = LAST_NAMES

    def __init__(self, size=None, **kwargs):
        max_size = len(self.first_names) * len(self.last_names)
        kwargs['size'] = size or max_size
        super(FullNameGenerator, self).__init__(**kwargs)
        if self.unique and not self.size == max_size and self.size > max_size / 4:
            raise RuntimeWarning("FullNameGenerator's performance will degrade at higher iteration counts when set to return unique results")

    def make_generator(self):
        while True:
            if len(self.hashes) == self.size:
                raise StopIteration
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            yield first_name, last_name


class SingleLineTextGenerator(BaseGenerator):
    size = 20
    words = WORD_LIST
    max_length = 80
    min_length = 50

    def make_generator(self):
        while True:
            title = ''
            length = random.randint(self.min_length, self.max_length)

            words = []
            while True:
                if not words:
                    words = random.sample(self.words, len(self.words) / 2 + 1)
                word = words.pop()
                if len(title) + len(word) + 1 > self.max_length:
                    break
                title += ' ' + word
                title = title.strip()
                if len(title) > length:
                    break
            yield title


class TitleGenerator(SingleLineTextGenerator):
    def make_generator(self):
        for title in super(TitleGenerator, self).make_generator():
            yield title[0].upper() + title[1:]


class SimplePasswordGenerator(RepeatValueGenerator):
    value = 'arstarst'


class GmailGenerator(RepeatValueGenerator):
    value = 'gmail'


class EmailAddressGenerator(MultiGenerator):
    format_string = '{username}@{domain}.com'
    generator_classes = {
            'username': UsernameGenerator,
            'domain': GmailGenerator,
            }
