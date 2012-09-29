import copy

from django.db import models

from foundry.base import DecimalGenerator
from foundry.generators import (BaseGenerator, UsernameGenerator,
        GmailAddressGenerator, BigIntegerGenerator, TrueGenerator,
        RandomBooleanGenerator, SingleLineTextGenerator,
        CurrentDateTimeGenerator, RandomIntegerGenerator, CurrentDateGenerator,
        FirstNameGenerator, LastNameGenerator)


class ModelGenerator(BaseGenerator):
    """
    Generates instances of a model
    """
    exclude = []
    fields = None
    model = None
    generator = None
    generators = {}

    def __init__(self, model=None, fields=None, exclude=None):
        if not model is None:
            self.model = model
        if not fields is None:
            self.fields = fields
        if not exclude is None:
            self.exclude = exclude
        self.setup_generators()
        # TODO: initialize hashes with database values to enforce uniqueness.

    def next(self, commit=False):
        instance = super(ModelGenerator, self).next()
        if commit:
            instance.save()
        return instance

    def generator(self):
        while True:
            kwargs = self.get_create_kwargs()
            yield self.model(**kwargs)

    def get_create_kwargs(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            if key in self.exclude:
                continue
            kwargs[key] = generator.next()
        return kwargs

    @classmethod
    def get_generator_for_field(cls, field):
        """
        Maps a field type to a Generator type.   Work in progress and lots of
        room for improvement.
        """
        if isinstance(field, models.AutoField):
            return None
        elif isinstance(field, models.BigIntegerField):
            return BigIntegerGenerator
        elif isinstance(field, models.BooleanField):
            if field.blank is False:
                return TrueGenerator
            elif not field.default == models.fields.NOT_PROVIDED:
                return None
            else:
                return RandomBooleanGenerator
        elif isinstance(field, models.CharField):
            if field.attname == 'username':
                return UsernameGenerator
            elif field.attname == 'email':
                return GmailAddressGenerator
            elif 'name' in field.attname:
                if 'first' in field.attname:
                    return FirstNameGenerator
                elif 'last' in field.attname:
                    return LastNameGenerator
                else:
                    return FirstNameGenerator
            elif not field.default == models.fields.NOT_PROVIDED:
                return None
            else:
                # TODO: max_length and min_length
                return SingleLineTextGenerator
        elif isinstance(field, models.DateField):
            return CurrentDateGenerator
        elif isinstance(field, models.DateTimeField):
            if field.auto_now or field.auto_now_add:
                return None
            elif not field.default == models.fields.NOT_PROVIDED:
                return None
            else:
                return CurrentDateTimeGenerator
        elif isinstance(field, models.DecimalField):
            raise DecimalGenerator
        elif isinstance(field, models.EmailField):
            return GmailAddressGenerator
        elif isinstance(field, models.FileField):
            raise NotImplementedError("Have not implemented FileGenerator")
        elif isinstance(field, models.FilePathField):
            raise NotImplementedError("Have not implemented FilePathGenerator")
        elif isinstance(field, models.FloatField):
            raise NotImplementedError("Have not implemented FloatGenerator")
        elif isinstance(field, models.ImageField):
            raise NotImplementedError("Have not implemented ImageGenerator")
        elif isinstance(field, models.IntegerField):
            return RandomIntegerGenerator
        elif isinstance(field, models.IPAddressField):
            raise NotImplementedError("Have not implemented IPAddressGenerator")
        elif isinstance(field, models.GenericIPAddressField):
            raise NotImplementedError("Have not implemented GenericIPAddressGenerator")
        elif isinstance(field, models.NullBooleanField):
            # TODO: Return ``None`` sometimes.
            if field.blank is False:
                return TrueGenerator
            elif not field.default == models.fields.NOT_PROVIDED:
                return None
            else:
                return RandomBooleanGenerator
        elif isinstance(field, models.PositiveIntegerField):
            return RandomIntegerGenerator
        elif isinstance(field, models.PositiveSmallIntegerField):
            return RandomIntegerGenerator
        elif isinstance(field, models.SlugField):
            raise NotImplementedError("Have not implemented SlugGenerator")
        elif isinstance(field, models.SmallIntegerField):
            return RandomIntegerGenerator
        elif isinstance(field, models.TextField):
            raise NotImplementedError("Have not implemented MultilineTextGenerator")
        elif isinstance(field, models.TimeField):
            raise NotImplementedError("Have not implemented TimeGenerator")
        elif isinstance(field, models.URLField):
            raise NotImplementedError("Have not implemented UrlGenerator")
        elif isinstance(field, models.ForeignKey):
            return cls(model=field.rel.to)
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")
        elif isinstance(field, models.OneToOne):
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")
        elif isinstance(field, models.ManyToMany):
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")

        raise NotImplementedError("Unknown field type: {0}".format(type(field)))

    def setup_generators(self):
        self.generators = copy.copy(self.generators)
        # Instantiate all manually defined generators.
        for key, Generator in self.generators.iteritems():
            self.generators[key] = Generator()
        for field in self.model._meta.fields:
            # Only declare fields if list of fields were declared.
            if self.fields and field.attname not in self.fields:
                continue
            # skip any manually declared generators
            if field.attname in self.generators:
                continue
            # skip if it is an excluded field
            if field.attname in self.exclude:
                continue
            # If we can leave this field blank, doit
            # Not sure if skipping on autocreated is needed.
            elif field.auto_created or field.blank and field.null:
                continue
            else:
                Generator = self.get_generator_for_field(field)
                if isinstance(Generator, BaseGenerator):
                    pass
                elif Generator is None:
                    continue
                elif issubclass(Generator, BaseGenerator):
                    self.generators[field.attname] = iter(Generator())
