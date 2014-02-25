from django.db import models

from perjury import generators as g


IGNORED_FIELDS = (models.AutoField, models.OneToOneField)


def get_generator_for_class(cls):
    """
    Recurses through the ``__bases__`` of a class to find the generator that
    corresponds with the field type.  If it finds none, it will raise an
    :class:`IndexError`.
    """
    # TODO: make this extensible???
    class2generator_map = {
            models.CharField: g.words,
            models.DateField: g.today,
            models.DateTimeField: g.now,
            models.DecimalField: g.decimal,
            models.EmailField: g.email,
            models.ForeignKey: ForeignKeyGenerator,
            models.IntegerField: g.smallint,
            models.TextField: g.words,
            models.TimeField: g.timenow,
            models.URLField: g.url,
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
    # TODO: make this extensible???
    name2generator_map = {
            'first_name': g.first_name,
            'last_name': g.last_name,
            'username': g.username,
            }

    return name2generator_map[name]


def get_generator_for_field(field):
    """
    Tries to figure out which generator to based on a Field instance.  If it
    cannot, it will raise a :class:`NotImplementedError`.
    """
    if field.choices:
        cls = g.Choice([choice[0] for choice in field.choices])
    else:
        try:
            cls = guess_generator_by_name(field.name)
        except KeyError:
            try:
                cls = get_generator_for_class(type(field))
            except IndexError:
                raise NotImplementedError('Unknown field type: {0}'.format(field))

        try:
            if issubclass(cls, FieldGenerator):
                return cls(field)
        except TypeError:
            pass

    return cls


def introspect_fields(fields):
    """
    For every field passed in, figure out the appropriate dictionary and return
    a dictionary of ``field.name`` goes to generator function.
    """
    generators = {}

    for field in fields:
        generators[field.name] = get_generator_for_field(field)

    return generators


class ModelGenerator(g.Generator):
    """
    Takes a model and creates a generator that will return instances of the
    model that have the data filled in.::

        from perjury.generators.django_models import ModelGenerator

        generator = ModelGenerator(MyModel)

        instance1 = generator()
        instance2 = generator()

    :class:`ModelGenerator` tries to intelligently pick generators for the
    model's fields.  If it picks incorrectly, or you have specific needs for a
    field, you may override it with by passing a dictionary of field name goes
    to callable in as the ``generators`` parameter.::

        from perjury.generators.django_models import ModelGenerator
        from perjury import generators as g

        def company_name():
            return '{0} {1}, Inc.'.format(
                g.first_name().captalize(),
                g.last_name().captalize()
                )

        generator = ModelGenerator(MyModel, generators={
            'company': company_name,
            })

        instance = generator()

    :class:`ModelGenerator` will by default skip any field that is in the
    ``exclude`` parameter, that is an instance of any class in
    ``IGNORED_FIELDS`` or that can be left empty.  Like ModelForm, if you wish
    to specify only the fields to generate, you can pass in the ``fields``
    parameter.::

        from perjury.django_models import ModelGenerator

        generator = ModelGenerator(User, fields=(
            'first_name',
            'last_name',
            'username',
            ))

        user = generator()

    If you don't wish for a field to have data generated for it, you can pass
    that in the ``exclude`` parameter.::

        from perjury.generators.django_models import ModelGenerator

        generator = ModelGenerator(User, exclude=('password',))

        user = generator()
        user.set_password('secret')
        user.save()

    """
    def __init__(self, model, generators=None, fields=None, exclude=tuple()):
        self.model = model

        fields_to_be_introspected = model._meta.fields

        # Limit fields to those that were specified.  ``fields`` is a list of
        # strings, we need to get the fields that correspond to those strings.
        if fields:
            def check(field):
                return field.name in fields
        else:
            def check(field): # NOQA
                if field.name in exclude:
                    return False
                elif isinstance(field, IGNORED_FIELDS) or \
                     field.blank or \
                     field.null:
                    return False
                return True

        fields_to_be_introspected = filter(check, fields_to_be_introspected)

        self.generators = introspect_fields(fields_to_be_introspected)

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
        """
        Builds a dictionary of field name goes to generated datum.  Exposed in
        case you need it for other purposes.
        """
        kwargs = {}

        for key, generator in self.generators.iteritems():
            kwargs[key] = generator()

        return kwargs


class FieldGenerator(g.Generator):
    """
    BaseClass for type checking.  Expects to have a field object passed into
    :method:`__init__`.
    """
    pass


class ForeignKeyGenerator(ModelGenerator, FieldGenerator):
    def __init__(self, field, *args, **kwargs):
        model = field.rel.to

        super(ForeignKeyGenerator, self).__init__(model, *args, **kwargs)
