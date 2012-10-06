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
            #models.ForeignKey: ForeignKeyGenerator,
            models.IntegerField: g.smallint,
            models.TextField: g.words,
            models.TimeField: g.timenow,
            models.URLField: g.url,
            models.BooleanField: g.truthy
            }

    try:
        return class2generator_map[cls]
    except KeyError:
        if cls.__bases__ and issubclass(cls.__bases__[0], models.Field):
            return get_generator_for_class(cls.__bases__[0])
        raise


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


class ModelGeneratorOptions(object):
    def __init__(self, meta):
        self.model = getattr(meta, 'model', None)
        self.fields = getattr(meta, 'fields', None)
        self.exclude = getattr(meta, 'exclude', None)


class ModelGeneratorMetaclass(type):
    def __new__(cls, name, bases, attrs):
        new_class = super(ModelGeneratorMetaclass, cls).__new__(cls, name, bases, attrs)

        # Shamefully stolen from django.forms.models.ModelFormMetaclass.
        #  - Allows for ModelGenerator to be declared and not throw errors
        #  about not havind a model assigned to it.
        try:
            parents = [b for b in bases if issubclass(b, ModelGenerator)]
        except NameError:
            # We are defining ModelGenerator itself.
            parents = None

        if parents is None:
            return new_class

        opts = new_class._meta = ModelGeneratorOptions(getattr(new_class, 'Meta', None))
        fields = []
        if opts.fields is None:
            # If opts fields is None, do all the fields we can.
            # - No: (in exclude), (
            #
            for field in opts.model._meta.fields:
                if opts.exclude is not None and field.attname in opts.exclude:
                    continue
                elif hasattr(new_class, field.attname):
                    continue
                elif type(field) in IGNORED_FIELDS:
                    continue
                fields.append(field)
        else:
            # If fields were explicitely declared, get those fields from
            # `model._meta.fields`
            for field in opts.model._meta.fields:
                if hasattr(new_class, field.attname):
                    continue
                if field.attname in opts.fields:
                    fields.append(field)

        generators = {}
        for field in fields:
            generator = get_generator_for_class(type(field))
            generators[field.attname] = generator
        new_class.generators = generators
        return new_class


class ModelGenerator(g.BaseGenerator):
    __metaclass__ = ModelGeneratorMetaclass

    def generator(self):
        kwargs = {}
        for key, generator in self.generators.iteritems():
            kwargs[key] = generator()
        return self._meta.model(**kwargs)
            

#class ModelGenerator(g.Generator):
#    """
#    Takes a model and creates a generator that will return instances of the
#    model that have the data filled in.::
#
#        from perjury.generators.django_models import ModelGenerator
#
#        generator = ModelGenerator(MyModel)
#
#        instance1 = generator()
#        instance2 = generator()
#
#    :class:`ModelGenerator` tries to intelligently pick generators for the
#    model's fields.  If it picks incorrectly, or you have specific needs for a
#    field, you may override it with by passing a dictionary of field name goes
#    to callable in as the ``generators`` parameter.::
#
#        from perjury.generators.django_models import ModelGenerator
#        from perjury import generators as g
#
#        def company_name():
#            return '{0} {1}, Inc.'.format(
#                g.first_name().captalize(),
#                g.last_name().captalize()
#                )
#
#        generator = ModelGenerator(MyModel, generators={
#            'company': company_name,
#            })
#
#        instance = generator()
#
#    :class:`ModelGenerator` will by default skip any field that is in the
#    ``exclude`` parameter, that is an instance of any class in
#    ``IGNORED_FIELDS`` or that can be left empty.  Like ModelForm, if you wish
#    to specify only the fields to generate, you can pass in the ``fields``
#    parameter.::
#
#        from perjury.django_models import ModelGenerator
#
#        generator = ModelGenerator(User, fields=(
#            'first_name',
#            'last_name',
#            'username',
#            ))
#
#        user = generator()
#
#    If you don't wish for a field to have data generated for it, you can pass
#    that in the ``exclude`` parameter.::
#
#        from perjury.generators.django_models import ModelGenerator
#
#        generator = ModelGenerator(User, exclude=('password',))
#
#        user = generator()
#        user.set_password('secret')
#        user.save()
#
#    """
#    def __init__(self, model, generators=None, fields=None, exclude=tuple()):
#        self.model = model
#
#        fields_to_be_introspected = model._meta.fields
#
#        # Limit fields to those that were specified.  ``fields`` is a list of
#        # strings, we need to get the fields that correspond to those strings.
#        if fields:
#            def check(field):
#                return field.name in fields
#        else:
#            def check(field): # NOQA
#                if field.name in exclude:
#                    return False
#                elif isinstance(field, IGNORED_FIELDS) or \
#                     field.blank or \
#                     field.null:
#                    return False
#                return True
#
#        fields_to_be_introspected = filter(check, fields_to_be_introspected)
#
#        self.generators = introspect_fields(fields_to_be_introspected)
#
#        if generators:
#            self.generators.update(generators)
#
#    def __call__(self, commit=False):
#        """
#        If ``commit`` is Truthy, the model instance will be saved.  ``commit``
#        defaults to False.
#        """
#        instance = self.model(**self.build_model_kwargs())
#
#        if commit:
#            instance.save()
#
#        return instance
#
#    def build_model_kwargs(self):
#        """
#        Builds a dictionary of field name goes to generated datum.  Exposed in
#        case you need it for other purposes.
#        """
#        kwargs = {}
#
#        for key, generator in self.generators.iteritems():
#            kwargs[key] = generator()
#
#        return kwargs
#
#
#class FieldGenerator(g.Generator):
#    """
#    BaseClass for type checking.  Expects to have a field object passed into
#    :method:`__init__`.
#    """
#    pass
#
#
#class ForeignKeyGenerator(ModelGenerator, FieldGenerator):
#    def __init__(self, field, *args, **kwargs):
#        model = field.rel.to
#
#        super(ForeignKeyGenerator, self).__init__(model, *args, **kwargs)
