from unittest import TestCase
import datetime
import decimal

from django.db import models

from perjury.generators.django_models import ModelGenerator
from perjury import generators as g


class CustomCharField(models.CharField):
    pass


class SimpleModel(models.Model):
    field1 = models.CharField(max_length=255)
    field2 = models.IntegerField()

    field3 = models.CharField(max_length=255, blank=True)
    field4 = models.IntegerField(blank=True, null=True)


class ModelWithLotsOfFields(models.Model):
    boolean = models.BooleanField()
    string = models.CharField(max_length=255)
    date = models.DateField()
    datetime = models.DateTimeField()
    decimal = models.DecimalField()
    email = models.EmailField()
    #file = models.FileField()
    #image = models.ImageField()
    text = models.TextField()
    time = models.TimeField()
    url = models.URLField()

    custom = CustomCharField()


class ChoiceFieldModel(models.Model):
    COLOR_CHOICES = (
        ('green', 'Green'),
        ('blue', 'Blue'),
        ('orange', 'Orange'),
    )
    color = models.CharField(max_length=255, choices=COLOR_CHOICES)


class TestModelGeneratorOptions(TestCase):
    Model = SimpleModel

    def test_required_generator(self):
        """
        By default only generate those fields that are required.
        """
        generator = ModelGenerator(self.Model)

        instance = generator()

        assert instance.field1
        # TODO: this is not future-proof is it?
        assert isinstance(instance.field1, basestring)

        assert instance.field2
        assert type(instance.field2) is int

        assert not instance.field3
        assert not instance.field4

    def test_fields_param(self):
        """
        If fields is passed in, should only generate those fields enumerated.
        """
        generator = ModelGenerator(self.Model, fields=('field1', 'field3'))

        instance = generator()

        assert instance.field1
        assert instance.field3

        assert not instance.field2
        assert not instance.field4

    def test_exclude_param(self):
        generator = ModelGenerator(self.Model, exclude=('field2',))

        instance = generator()

        assert instance.field1

        assert not instance.field2
        assert not instance.field3
        assert not instance.field4

    def test_override_generators(self):
        generator = ModelGenerator(self.Model, generators={
            'field2': g.email,
            'field3': g.smallint,
            })

        instance = generator()

        assert '@example.com' in instance.field2

        assert type(instance.field3) is int


class TestFieldMatching(TestCase):
    Model = ModelWithLotsOfFields

    def test_builtin_field_types(self):
        generator = ModelGenerator(self.Model)

        instance = generator()

        assert instance.boolean in (True, False)
        assert isinstance(instance.string, basestring)
        assert isinstance(instance.date, datetime.date)
        assert isinstance(instance.datetime, datetime.datetime)
        assert isinstance(instance.decimal, decimal.Decimal)
        assert '@example.com' in instance.email
        assert isinstance(instance.text, basestring)
        assert isinstance(instance.time, datetime.time)
        # TODO: validate url with urllib???  That test would probably live in
        # the generators tests and not in here, we are just making sure field
        # types are supported
        assert 'http' in instance.url

    def test_custom_field_types(self):
        generator = ModelGenerator(self.Model)

        instance = generator()

        assert isinstance(instance.custom, basestring)


class TestChoiceField(TestCase):
    def test_choice_field(self):
        generator = ModelGenerator(ChoiceFieldModel)
        choices = [choice[0] for choice in ChoiceFieldModel.COLOR_CHOICES]

        for i in range(1, 1000):
            instance = generator()
            assert instance.color in choices
