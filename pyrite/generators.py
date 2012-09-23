"""
Future plans

1. Ability to randomize a generators return values.
"""
import random
from itertools import product
from polls.content import (MALE_NAMES, FEMALE_NAMES, LAST_NAMES, FIRST_NAMES,
        WORD_LIST, USERNAMES)


class BaseGenerator(object):
    def __init__(self, size=None):
        if size is not None:
            self.size = size


class BaseNameGenerator(BaseGenerator):
    """
    >>> n = NameGenerator()
    >>> for name in n:
    >>>     print name

    Prints as many unique names as name generator can produce

    >>> n = NameGenerator(20)
    >>> for name in n:
    >>>     print name

    Prints 20 names
    """
    names = []

    def __init__(self, size=None, names=None):
        if names is not None:
            self.names = names

        if size is not None:
            self.size = size
        else:
            self.size = len(self.names)

    def __iter__(self):
        for i in xrange(self.size):
            yield self.names[i]

    def __len__(self):
        return self.size

    def __getitem__(self, key):
        return self.names[key]


class NameGenerator(BaseNameGenerator):
    """
    TODO: shuffle the names
    """
    names = FIRST_NAMES


class MaleNameGenerator(BaseNameGenerator):
    names = MALE_NAMES


class FemaleNameGenerator(BaseNameGenerator):
    names = FEMALE_NAMES


class LastNameGenerator(BaseNameGenerator):
    names = LAST_NAMES


class UsernameGenerator(BaseNameGenerator):
    names = USERNAMES


class FullNameGenerator(BaseNameGenerator):
    first_names = FIRST_NAMES
    last_names = LAST_NAMES

    def __init__(self, size=None, first_names=None, last_names=None):
        if first_names is None:
            first_names = self.first_names
        if last_names is None:
            last_names = self.last_names
        names = product(first_names, last_names)

        if size is None:
            size = len(first_names) * len(last_names)
        super(FullNameGenerator, self).__init__(size, names)

    def __iter__(self):
        for i, name in enumerate(self.names):
            if i >= self.size:
                return
            yield name

    def __getitem__(self, key):
        raise TypeError('FullNameGenerator does not support indexind')


class SingleLineTextGenerator(BaseGenerator):
    size = 20
    words = WORD_LIST
    max_length = 80
    min_length = 50

    def __init__(self, size=None, max_length=None, min_length=None, words=None):
        if max_length is not None:
            self.max_length = max_length
        if min_length is not None:
            self.min_length = min_length
        if words is not None:
            self.words = words
        super(SingleLineTextGenerator, self).__init__(size)

    def __iter__(self):
        for i in xrange(self.size):
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
    def __iter__(self):
        for title in super(TitleGenerator, self).__iter__():
            yield title[0].upper() + title[1:]


class RepeatValueGenerator(BaseGenerator):
    """
    Returns the same value over and over
    """
    value = None

    def __init__(self, size, value=None):
        super(RepeatValueGenerator, self).__init__(size)
        if value is not None:
            self.value = value

    def __iter__(self):
        for i in xrange(self.size):
            yield self.value


class SimplePasswordGenerator(RepeatValueGenerator):
    value = 'arstarst'


class MultiGenerator(BaseGenerator):
    """
    Uses multiple generators to generate a string formatted value
    """
    generators = {}
    generator_classes = []
    format_string = None

    def __init__(self, size):
        super(MultiGenerator, self).__init__(size)
        for key, GeneratorClass in self.generator_classes.iteritems():
            self.generators[key] = GeneratorClass(self.size).__iter__()

    def __iter__(self):
        for i in xrange(self.size):
            kwargs = self.get_format_kwargs()
            retval = self.format_string.format(**kwargs)
            yield retval

    def get_format_kwargs(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator.next()
        return kwargs


class GmailGenerator(RepeatValueGenerator):
    value = 'gmail'


class EmailAddressGenerator(MultiGenerator):
    format_string = '{username}@{domain}.com'
    generator_classes = {
            'username': UsernameGenerator,
            'domain': UsernameGenerator,
            }


class ModelGenerator(BaseGenerator):
    """
    Generates instances of a model
    """
    fields = []
    model = None
    generators = {}

    def __init__(self, size):
        super(ModelGenerator, self).__init__(size)
        self.setup_generators()

    def __iter__(self):
        for i in range(self.size):
            kwargs = self.get_create_kwargs()
            yield self.create_model(**kwargs)

    def setup_generators(self):
        for field_name, GeneratorClass in self.fields:
            self.generators[field_name] = GeneratorClass(self.size).__iter__()

    def get_create_kwargs(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator.next()
        return kwargs

    def create_model(self, **kwargs):
        instance = self.model.oblects.create(**kwargs)
        return instance
