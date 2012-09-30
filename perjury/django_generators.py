from django.db import models

from perjury import generators


IGNORED_FIELDS = (models.AutoField, models.OneToOneField)


def get_generator_for_class(cls):
    """
    Recurses through the ``__bases__`` of a class to find the generator that
    corresponds with the field type.  If it finds none, it will raise an
    :class:`IndexError`.
    """
    class2generator_map = {
            models.CharField: generators.words,
            models.DateTimeField: generators.now,
            models.ForeignKey: ForeignKeyGenerator,
            models.IntegerField: generators.smallint,
            models.TextField: generators.words,
            models.EmailField: generators.email,
            }

    try:
        return class2generator_map[cls]
    except KeyError:
        return get_generator_for_class(cls.__bases__[0])


def guess_generator_by_name(name):
    """
    Tries to intelligently guess a generator based on a name.  If it cannot, it
    will raise a :class:`KeyError`.
    """
    name2generator_map = {
            'first_name': generators.first_name,
            'last_name': generators.last_name,
            'username': generators.username,
            }

    return name2generator_map[name]


def get_generator_for_field(field):
    """
    Tries to figure out which generator to based on a Field instance.  If it
    cannot, it will raise a :class:`NotImplementedError`.
    """
    try:
        cls = guess_generator_by_name(field.name)
    except KeyError:
        try:
            cls = get_generator_for_class(type(field))
        except IndexError:
            raise NotImplementedError('Unknown field type: {0}'.format(field))

    if isinstance(cls, FieldGenerator):
        return cls(field)
    else:
        return cls


def introspect_fields(fields, exclude=None):
    """
    For almost every field, figure out the appropriate dictionary and return a
    dictionary of ``field.name`` goes to generator function.  It will skip
    any field that is in the ``exclude`` parameter, that is an instance of
    any class in ``IGNORED_FIELDS`` or that can be left empty.
    """
    if exclude is None:
        exclude = tuple()

    generators = {}

    for field in fields:
        if field.name in exclude:
            continue

        if isinstance(field, IGNORED_FIELDS) or field.blank or field.null:
            continue

        print field.name, field.model

        generators[field.name] = get_generator_for_field(field)

    return generators


class FieldGenerator(generators.Generator):
    """
    BaseClass for type checking.
    """
    pass


class ModelGenerator(FieldGenerator):
    """
    Takes a model and creates a generator that will return instances of the
    model that have the data filled in.::

        from perjury.django_generators import ModelGenerator

        generator = ModelGenerator(MyModel)

        instance1 = generator()
        instance2 = generator()

    :class:`ModelGenerator` tries to intelligently pick generators for the
    model's fields.  If it picks incorrectly, or you have specific needs for a
    field, you may override it with by passing a dictionary of field name goes
    to callable in as the ``generators`` parameter.::

        from perjury.django_generators import ModelGenerator
        from perjury import generators as g

        def full_name():
            return ' '.join((g.first_name(), g.last_name()))

        generator = ModelGenerator(MyModel, generators={
            'full_name': full_name,
            })

        instance = generator()

    Like ModelForm, if you wish to specify only the fields to generate, you can
    pass in the ``fields`` parameter.::

        from perjury.django_generators import ModelGenerator

        generator = ModelGenerator(User, fields=(
            'first_name',
            'last_name',
            'username',
            ))

        user = generator()

    If you don't wish for a field to have data generated for it, you can pass
    that in the ``exclude`` parameter.::

        from perjury.django_generators import ModelGenerator

        generator = ModelGenerator(User, exclude=('password',))

        user = generator()
        user.set_password('secret')
        user.save()

    """
    def __init__(self, model, generators=None, fields=None, exclude=None):
        self.model = model

        fields_to_be_introspected = model._meta.fields

        # Limit fields to those that were specified.  ``fields`` is a list of
        # strings, we need to get the fields that correspond to those strings.
        if fields:
            fields_to_be_introspected = filter(
                    lambda field: field.name in fields,
                    fields_to_be_introspected
                    )

        self.generators = introspect_fields(fields_to_be_introspected, exclude)

        if generators:
            self.generators.update(generators)

    def __call__(self, commit=False):
        """
        If ``commit`` is Truthy, the model instance will be saved.  ``commit``
        defaults to False.
        """
        instance = self.model(**self.build_model_kwargs())

        if commit:
            instance.save()

        return instance

    def build_model_kwargs(self):
        kwargs = {}

        for key, generator in self.generators.iteritems():
            kwargs[key] = generator()

        return kwargs


class ForeignKeyGenerator(ModelGenerator):
    def __init__(self, field, *args, **kwargs):
        model = field.rel.to

        super(ForeignKeyGenerator, self).__init__(model, *args, **kwargs)
