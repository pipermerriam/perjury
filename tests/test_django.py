from unittest import TestCase

from django.db import models

from perjury.django_generators import ModelGenerator
from perjury import generators as g


class TestModelGeneratorOptions(TestCase):
    def setUp(self):
        class A(models.Model):
            field1 = models.CharField(max_length=255)
            field2 = models.IntegerField()

            field3 = models.CharField(max_length=255, blank=True)
            field4 = models.IntegerField(blank=True, null=True)

        self.A = A

    def test_required_generator(self):
        """
        By default only generate those fields that are required.
        """
        generator = ModelGenerator(self.A)

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
        generator = ModelGenerator(self.A, fields=('field1', 'field3'))

        instance = generator()

        assert instance.field1
        assert instance.field3

        assert not instance.field2
        assert not instance.field4

    def test_exclude_param(self):
        generator = ModelGenerator(self.A, exclude=('field2',))

        instance = generator()

        assert instance.field1

        assert not instance.field2
        assert not instance.field3
        assert not instance.field4

    def test_override_generators(self):
        generator = ModelGenerator(self.A, generators={
            'field2': g.email,
            'field3': g.smallint,
            })

        instance = generator()

        assert '@example.com' in instance.field2

        assert type(instance.field3) is int
