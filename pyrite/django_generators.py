import copy

from pyrite.generators import (BaseGenerator, UsernameGenerator, SimplePasswordGenerator,
        EmailAddressGenerator, BigIntegerGenerator, TrueGenerator,
        RandomBooleanGenerator, SingleLineTextGenerator,
        CurrentDateTimeGenerator, RandomIntegerGenerator, CurrentDateGenerator)


class ModelGenerator(BaseGenerator):
    """
    Generates instances of a model
    """
    exclude = []
    fields = []
    model = None
    generator = None
    generators = {}

    def __init__(self, size):
        super(ModelGenerator, self).__init__(size)
        self.setup_generators()

    def __iter__(self):
        for i in range(self.size):
            kwargs = self.get_create_kwargs()
            yield self.create_model(**kwargs)

    @classmethod
    def get_generator_for_field(self, field):
        """
        Maps a field type to a Generator type.   Work in progress and lots of
        room for improvement.
        """
        from django.db import models

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
                return EmailAddressGenerator
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
                return CurrentDatetimeGenerator
        elif isinstance(field, models.DecimalField):
            raise NotImplementedError("Have not implemented DecimalGenerator")
        elif isinstance(field, models.EmailField):
            return EmailAddressGenerator
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
        elif isinstance(field, models.UrlField):
            raise NotImplementedError("Have not implemented UrlGenerator")
        elif isinstance(field, models.ForeignKey):
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")
        elif isinstance(field, models.OneToOne):
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")
        elif isinstance(field, models.ManyToMany):
            raise NotImplementedError("Have not implemented Ability to auto create more model generators.")

        raise NotImplementedError("Unknown field type: {0}".format(type(field)))

    def setup_generators(self):
        self.generators = copy.copy(self.generators)
        # Instantiate all manually defined generators.
        for key, Generator in self.generators:
            self.generators[key] = Generator(self.size)
        for field in self.model._meta.fields:
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
                if Generator is None:
                    continue
                self.generators[field.attname] = iter(Generator(self.size))

    def get_create_kwargs(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator.next()
        return kwargs

    def create_model(self, **kwargs):
        instance = self.model.oblects.create(**kwargs)
        return instance

#from django.contrib.auth.models import User

#class UserGenerator(ModelGenerator):
#    """
#    Not quite here yet.
#    """
#    fields = (
#            ('username', UsernameGenerator),
#            ('password', SimplePasswordGenerator),
#            ('email', EmailAddressGenerator),
#            )
#    model = User
#
#    def __init__(self, *args, **kwargs):
#        super(UserGenerator, self).__init__(*args, **kwargs)
#        self.name_generator = FullNameGenerator(self.size).__iter__()
#
#    def create_model(self, **kwargs):
#        user = User.objects.create_user(**kwargs)
#        user.first_name, user.last_name = self.name_generator.next()
#        user.save()
#        return user
