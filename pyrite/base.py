import random
from itertools import repeat


class BaseGenerator(object):
    """
    Base class for all pyrite generator classes.
    """
    size = None
    unique = True
    shuffle = True

    def __init__(self, size=None, unique=None, shuffle=None):
        self.hashes = set()
        self.size = size or self.size
        self.unique = unique or self.unique
        self.shuffle = shuffle or self.shuffle

    def __len__(self):
        return self.size

    def compute_hash(self, value):
        return value

    def make_generator(self):
        """
        Hook for subclasses of `BaseGenerator`.
        """
        raise NotImplementedError('Genertator classes must implement their own `make_generator` method.')

    def __iter__(self):
        """
        """
        generator = self.make_generator()
        for i in xrange(self.size):
            # Enter an infinite loop, allowing us to ensure values are unique
            # if self.unique is set to true
            while True:
                retval = generator.next()
                hash = self.compute_hash(retval)
                # Break if the hash for this return value is in self.hashes.
                if not hash in self.hashes:
                    break
            # If unique return values are being enforced, add the hash to
            # self.hashes.  Otherwise, leaving it out will allow for duplicate
            # return values.
            if self.unique:
                self.hashes.add(hash)
            yield retval


class WordGenerator(BaseGenerator):
    """
    Generates results based on a wordlist.
    """
    words = []

    def __init__(self, size=None, **kwargs):
        kwargs['size'] = size or len(self.words)
        super(WordGenerator, self).__init__(**kwargs)
        if self.shuffle:
            # Make the list of words mutable if it appears to be immutable
            if not hasattr(self.words, '__setitem__'):
                self.words = list(self.words)
            random.shuffle(self.words)

    def make_generator(self):
        return iter(self.words)

    def __getitem__(self, key):
        return self.words[key]


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
            self.generators[key] = iter(GeneratorClass(self.size))

    def make_generator(self):
        while True:
            kwargs = self.get_format_kwargs()
            retval = self.format_string.format(**kwargs)
            yield retval

    def get_format_kwargs(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator.next()
        return kwargs


class RepeatValueGenerator(BaseGenerator):
    """
    Returns the same value over and over
    """
    unique = False
    value = None

    def make_generator(self):
        return repeat(self.value)
