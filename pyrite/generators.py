import random
import datetime

from pyrite.base import (BaseGenerator, WordGenerator, MultiGenerator,
        RepeatValueGenerator, IntegerGenerator, RandomChoiceGenerator,
        DateTimeGenerator, CoercionGenerator)
from pyrite.content import (MALE_NAMES, FEMALE_NAMES, LAST_NAMES, FIRST_NAMES,
        WORD_LIST, USERNAMES)


class MaleNameGenerator(WordGenerator):
    """
    Generates male names from a wordlist of common male names.
    """
    words = MALE_NAMES


class FemaleNameGenerator(WordGenerator):
    """
    Generates female names from a wordlist of common female names.
    """
    words = FEMALE_NAMES


class FirstNameGenerator(WordGenerator):
    """
    Generates first names from a wordlist of common male and female names.
    """
    words = FIRST_NAMES


class LastNameGenerator(WordGenerator):
    """
    Generates last names from a wordlist of common last names.
    """
    words = LAST_NAMES


class UsernameGenerator(WordGenerator):
    """
    Generates usernames from a wordlist of common usernames.
    """
    words = USERNAMES


class FullNameGenerator(BaseGenerator):
    """
    Generates 2-tuples of first_name, last_name pairs from a wordlist of common
    names.
    """
    first_names = FIRST_NAMES
    last_names = LAST_NAMES

    def __init__(self, size=None, **kwargs):
        max_size = len(self.first_names) * len(self.last_names)
        kwargs['size'] = size or max_size
        super(FullNameGenerator, self).__init__(**kwargs)
        if self.unique and not self.size == max_size and self.size > max_size / 4:
            raise RuntimeWarning("FullNameGenerator's performance will degrade at higher iteration counts when set to return unique results")

    def inner_generator(self):
        while True:
            if len(self.hashes) == self.size:
                raise StopIteration
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            yield first_name, last_name


class SingleLineTextGenerator(BaseGenerator):
    """
    Returns single lines of text between ``self.min_length`` and
    ``self.max_length`` in length.
    """
    size = 20
    words = WORD_LIST
    max_length = 80
    min_length = 50

    def inner_generator(self):
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
    """
    Returns the same valus as ``SingleLineTextGenerator`` but with their first
    letter capitalized.
    """
    def inner_generator(self):
        for title in super(TitleGenerator, self).inner_generator():
            yield title[0].upper() + title[1:]


class SimplePasswordGenerator(RepeatValueGenerator):
    value = 'arstarst'


class TrueGenerator(RepeatValueGenerator):
    """
    Generates ``True`` until termination
    """
    value = True


class FalseGenerator(RepeatValueGenerator):
    """
    Generates ``False`` until termination
    """
    value = False


class RandomBooleanGenerator(RandomChoiceGenerator):
    """
    Returns ``True`` or ``False`` randomly
    """
    values = [True, False]


class GmailGenerator(RepeatValueGenerator):
    value = 'gmail'


class EmailAddressGenerator(MultiGenerator):
    """
    Returns gmail addresses using ``UsernameGenerator`` for the username
    portion of the email address.
    """
    format_string = '{username}@{domain}.com'
    generator_classes = {
            'username': UsernameGenerator,
            'domain': GmailGenerator,
            }


class OrderedIntegerGenerator(IntegerGenerator):
    """
    Returns ordered integers over the range ``self.lower_bound``,
    ``self.upper_bound``, repeating until termination
    """
    shuffle = False


class BigIntegerGenerator(IntegerGenerator):
    """
    Generates 64-bit integers between -9223372036854775808 and 9223372036854775807
    """
    lower_bound = -9223372036854775808
    upper_bound = 9223372036854775807


class RandomIntegerGenerator(IntegerGenerator):
    """
    Returns random integers over the range ``self.lower_bound``,
    ``self.upper_bound``, repeating until termination
    """
    pass


class CurrentDateTimeGenerator(DateTimeGenerator):
    """
    Generates datetimes within a certain range of the current time.
    """
    delta_days = 30

    def get_min_datetime(self):
        return datetime.datetime.now() - datetime.timedelta(days=self.delta_days)

    def get_max_datetime(self):
        return datetime.datetime.now() + datetime.timedelta(days=self.delta_days)


class CurrentDateGenerator(CoercionGenerator):
    """
    Generates dates within a certain range of the current time.
    """
    generator_class = CurrentDateTimeGenerator

    def coerce_value(self, value):
        return value.date
