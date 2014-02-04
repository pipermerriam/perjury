class BaseResource(object):
    """
    Base class for all foundry generator classes.
    """
    def __init__(self, generator):
        self.generator = iter(generator)

    def next(self):
        return next(self.generator)

    def __call__(self):
        return next(self)

    def __iter__(self):
        while True:
            yield next(self)


class CombinedResource(object):
    def __init__(self, *args, **kwargs):
        self.positional_generators = args
        self.named_generators = kwargs

    def combine_values(self, *args, **kwargs):
        raise NotImplemented('Subclasses must implement the `combine_values` '
                             'method')

    def next(self):
        return self.combine_values(
            *(
                g() for g in self.positional_generators
            ),
            **dict(
                (k, v()) for k, v in self.named_generators.iteritems()
            )
        )

    def __call__(self):
        return next(self)

    def __iter__(self):
        while True:
            yield next(self)


class FormattedStringResource():
    template = None

    def combine_values(self, *args, **kwargs):
        if self.template is None:
            raise AttributeError('`FormattedStringResource` requires a `template` '
                                 'string.')
        return self.template.format(*args, **kwargs)
