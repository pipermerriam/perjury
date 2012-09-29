from __future__ import division
import random
import copy
import datetime
import time

from decimal import Decimal
from itertools import repeat

from foundry.exceptions import UniqueValueTimeoutError


class BaseGenerator(object):
    """
    Base class for all foundry generator classes.

    :attr:`~BaseGenerator.size`

    If set to ``None``, this generator will never cease iteration.  Otherwise,
    :attr:`~BaseGenerator.size` will determine the number of values returnes
    during iteration.
    """
    MAX_HANG_TIME = 1.0
    size = None
    unique = True
    shuffle = True
    hashes = set()

    def __init__(self):
        self.initialize_hashes()

    def initialize_hashes(self):
        self.hashes = copy.copy(self.hashes)

    def get_hash_function(self):
        """
        Hook for ensuring that when :attr:`~BaseGenerator.unique`, the
        generator will return unique values.

        During generation when :attr:`~BaseGenerator.unique` is ``True``, the
        generator stores a hash of all of the values it has already returned.
        When it encounters a value it has already come across, if will spend a
        brief amount of time continuing to try and find a value it has not
        already seen by continuing to iterate through the `inner_generator``.
        """
        return hash

    def generator(self):
        """
        This method must be implemented on subclasses of ``BaseGenerator``.
        This method should return an iterator with a few caveats.

        Due to the way uniqueness is handled in foundry generators, when
        possible, this method should return a generator which can return as
        many values as possible.  In situations where it is attainable, an
        'infinite generator' should be returned since limiting iterations is
        handled in :func:`~BaseGenerator.outer_generator`.
        """
        raise NotImplementedError('Genertator classes must implement their own `inner_generator` method.')

    @property
    def inner_generator(self):
        if not hasattr(self, '_generator'):
            self.reset()
        return self._generator

    def outer_generator(self):
        hash_function = self.get_hash_function()
        generator = self.generator()
        while True:
            last_yield = None
            while True:
                if last_yield is None:
                    last_yield = time.time()
                if time.time() - last_yield > self.MAX_HANG_TIME:
                    raise UniqueValueTimeoutError('Took longer than {self.MAX_HANG_TIME} seconds attempting to generate a unique value')
                retval = generator.next()
                hash = hash_function(retval)
                # Break if the hash for this return value is in self.hashes.
                if not hash in self.hashes:
                    break
            # If unique return values are being enforced, add the hash to
            # self.hashes.  Otherwise, leaving it out will allow for duplicate
            # return values.
            if self.unique:
                self.hashes.add(hash)
            yield retval

    def reset(self):
        self._generator = self.outer_generator()

    def next(self):
        """
        In the case of :attr:`BaseGenerator.size` being set to ``None``, this
        will return an infinite generator.  With certain subclasses, this may
        have undocumented or unpredictable results at very high iteration
        counts.

        In the case of a fixed size, this returns an iterator which will
        terminate after :attr:`BaseGenerator.size` iterations.
        """
        return self.inner_generator.next()

    def __call__(self, *args, **kwargs):
        """
        Wrapper around :func:`BaseGenerator.next`
        """
        return self.next(*args, **kwargs)

    def __iter__(self):
        """
        Implements the actual generation, limiting based on ``self.size`` if
        present, and ensuring that unique values are returned if
        ``self.unique`` is set to ``True``.
        """
        return self.inner_generator


class TestSubclass(BaseGenerator):
    def generator(self):
        i = 0
        while True:
            yield i
            i += 1


class WordGenerator(BaseGenerator):
    """
    Generates results based on a wordlist stored in self.words.
    """
    # TODO: figuer out how to combine this properly with RandomChoiceGenerator.
    words = []

    def __init__(self):
        super(WordGenerator, self).__init__()
        if self.shuffle:
            # Make the list of words mutable if it appears to be immutable
            if not hasattr(self.words, '__setitem__'):
                self.words = list(self.words)
            random.shuffle(self.words)

    def generator(self):
        for word in self.words:
            yield word


class MultiGenerator(BaseGenerator):
    """
    Uses multiple generators to generate the kwargs for a string formatter.

    :attr:`~generators`

    dictionary of generator classes to be in
    :func:`MultiGenerator.get_format_kwargs` to be used in string formatting.
    """
    generators = {}
    format_string = None

    def __init__(self):
        super(MultiGenerator, self).__init__()
        self.generators = copy.copy(self.generators)
        for key, GeneratorClass in self.generators.iteritems():
            self.generators[key] = iter(GeneratorClass())

    def generator(self):
        while True:
            kwargs = self.get_format_kwargs()
            retval = self.format_string.format(**kwargs)
            yield retval

    def get_format_kwargs(self):
        """
        Returns a dictionary with an entry for each entry generator declared in
        the class.
        """
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator.next()
        return kwargs


class RepeatValueGenerator(BaseGenerator):
    """
    Generates the same value for each iteration.  This is simply a wrapper
    around :func:`itertools.repeat`.
    """
    unique = False
    value = None

    def __init__(self, value=None):
        super(RepeatValueGenerator, self).__init__()
        if value is not None:
            self.value = value

    def generator(self):
        return repeat(self.value)


class IntegerGenerator(BaseGenerator):
    """
    Base class for integer generation.

    :attr:`~IntegerGenerator.shuffle`

    If set to ``True`` the generator will return ordered values.  The following
    subclass and ``range(20)`` will return the same values.

    .. code-block:: python

        class YearGenerator(IntegerGenerator):
            shuffle = False
            lower_bound = 2000
            upper_bound = 2010

        x = [value for value in YearGenerator(20)]
        # [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
        y = range(2000, 2010)
        # [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]
        assert(x == y) # succeeds

    If set to ``False``, the generator will return values randomly selected
    between :attr:`~IntegerGenerator.lower_bound` and
    :attr:`~IntegerGenerator.upper_bound`

    .. code-block:: python

        class TeenAgeGenerator(IntegerGenerator):
            lower_bound = 13
            upper_bound = 20

        x = [value for value in AgeGenerator(10)
        # [17, 20, 18, 18, 13, 15, 14, 16, 16, 19]

    If :attr:`~IntegerGenerator.unique` and :attr:`~IntegerGenerator.shuffle`
    are both set to ``False``, the generator will repeat over the values in its
    range in numeric order.

    .. code-block:: python

        class NumberCycleGenerator(IntegerGenerator):
            lower_bound = 10
            upper_bound = 15

        x = [value for value in NumberCycleGenerator(10)
        # [10, 11, 12, 13, 14, 10, 11, 12, 13, 14]

    :attr:`~IntegerGenerator.unique`

    If set to ``True``, the generator will validate that it is able to return
    enough values.

    :attr:`~IntegerGenerator.lower_bound`

    Sets the inclusive lower bound for return values for the generator.

    :attr:`~IntegerGenerator.upper_bound`

    Sets the non-inclusive upper bound for return values for the generator.
    """
    unique = False
    lower_bound = 0
    upper_bound = 1000

    def __init__(self, **kwargs):
        super(IntegerGenerator, self).__init__()
        for field_name in ['lower_bound', 'upper_bound', 'unique', 'shuffle']:
            value = kwargs.pop(field_name, None)
            if value is not None:
                setattr(self, field_name, int(value))
        if self.unique and self.size > abs(self.upper_bound - self.lower_bound):
            raise ValueError('Impossible constraints.  Either disable uniqueness on this generator, or increase the bounds')

    def generator(self):
        while True:
            if self.shuffle:
                yield random.randint(self.lower_bound, self.upper_bound)
            else:
                for i in xrange(self.lower_bound, self.upper_bound):
                    yield i


class RandomChoiceGenerator(BaseGenerator):
    """
    Generates a random choice from a pre-defined list of choices.
    """
    # TODO: reconcile this generator and WordGenerator
    unique = False
    values = []

    def generator(self):
        while True:
            yield random.choice(self.values)


class DateTimeGenerator(BaseGenerator):
    """
    Base class for date and datetime generation.
    """
    # TODO: make shuffle do something.  Equally spaced ordered dates possibly?
    min_datetime = datetime.datetime.min
    max_datetime = datetime.datetime.max

    def get_min_datetime(self):
        return self.min_datetime

    def get_max_datetime(self):
        return self.max_datetime

    def generator(self):
        while True:
            delta = self.get_max_datetime() - self.get_min_datetime()
            seconds = int(delta.total_seconds())
            yield self.get_min_datetime() + datetime.timedelta(seconds=random.randrange(seconds))


class CoercionGenerator(BaseGenerator):
    """
    Generator base class which returns coerced values from another generator.
    """
    generator_class = None

    def coerce_value(self, value):
        raise NotImplementedError('Subclasses of CoercionGenerator must implement a `coerce_value` method')

    def generator(self):
        if self.generator_class is None:
            raise NotImplementedError('Subclasses of CoercionGenerator must define a `generator_class`')
        generator = self.generator_class()
        for value in generator:
            yield self.coerce_value(value)


class DecimalGenerator(BaseGenerator):
    lower_bound = 0
    upper_bound = 100
    precision = 2

    def __init__(self, upper_bound=None, lower_bound=None, precision=None):
        super(DecimalGenerator, self).__init__()
        self.upper_bound = upper_bound or self.upper_bound
        self.lower_bound = lower_bound or self.lower_bound
        self.precision = precision or self.precision

    def generator(self):
        divisor = 10 ** self.precision
        value = random.randint(divisor * self.upper_bound)
        return Decimal(value) / divisor
