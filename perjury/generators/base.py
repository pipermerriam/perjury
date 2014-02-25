import random


class BaseResource(object):
    """
    Base class for all foundry generator classes.
    """
    @property
    def generator(self):
        raise AttributeError('Resources must have a `generator`')

    def next(self):
        return next(self.generator)

    def __call__(self):
        return next(self)

    def __iter__(self):
        while True:
            yield next(self)

    def __mul__(self, other):
        return [next(self) for i in xrange(other)]


class SimpleResource(BaseResource):
    generator = None

    def __init__(self, source, shuffle=True):
        self.source = source
        self.generator = iter(source)


class CombinedResource(BaseResource):
    def __init__(self, *args, **kwargs):
        self.positional_generators = args
        self.named_generators = kwargs

    @property
    def generator(self):
        while True:
            yield self.combine_values(
                *(
                    g() for g in self.positional_generators
                ),
                **dict(
                    (k, v()) for k, v in self.named_generators.iteritems()
                )
            )

    def combine_values(self, *args, **kwargs):
        raise NotImplemented('Subclasses must implement the `combine_values` '
                             'method')


class FormattedStringResource(CombinedResource):
    template = None

    def combine_values(self, *args, **kwargs):
        if self.template is None:
            raise AttributeError('`FormattedStringResource` requires a `template` '
                                 'string.')
        return self.template.format(*args, **kwargs)
