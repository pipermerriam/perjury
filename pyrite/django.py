from pyrite import (BaseGenerator, UsernameGenerator, SimplePasswordGenerator,
        EmailAddressGenerator)
from django.contrib.auth.models import User


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


class UserGenerator(ModelGenerator):
    """
    Not quite here yet.
    """
    fields = (
            ('username', UsernameGenerator),
            ('password', SimplePasswordGenerator),
            ('email', EmailAddressGenerator),
            )
    model = User

    def __init__(self, *args, **kwargs):
        super(UserGenerator, self).__init__(*args, **kwargs)
        self.name_generator = FullNameGenerator(self.size).__iter__()

    def create_model(self, **kwargs):
        user = User.objects.create_user(**kwargs)
        user.first_name, user.last_name = self.name_generator.next()
        user.save()
        return user
