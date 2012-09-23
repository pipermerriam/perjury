"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from unittest import TestCase

from polls.generators import (BaseNameGenerator, NameGenerator,
        MaleNameGenerator, FemaleNameGenerator, LastNameGenerator,
        FullNameGenerator, SingleLineTextGenerator, TitleGenerator)


class TestNameGenerators(TestCase):
    def setUp(self):
        self.names = ['joe', 'jim', 'john']

    def test_base_name_generator(self):
        g = BaseNameGenerator(names=self.names)
        self.assertEqual(len(g), 3)

    def test_base_name_generator_slicing(self):
        g = BaseNameGenerator(names=self.names)
        names = g[1:3]
        self.assertEqual(names, self.names[1:3])

    def test_base_name_generator_custom_length(self):
        g = BaseNameGenerator(size=2, names=self.names)
        self.assertEqual(len(g), 2)
        names = [name for name in g]
        self.assertEqual(len(names), 2)
        self.assertEqual(names, self.names[:2])

    def test_name_generator_classes(self):
        for NameGeneratorClass in [NameGenerator, MaleNameGenerator,
                FemaleNameGenerator, LastNameGenerator]:
            g = NameGeneratorClass()
            self.do_assertions(g)

    def do_assertions(self, generator):
        self.assertEqual(len(generator), len(generator.names))
        for name in generator:
            self.assertIn(name, generator.names)


class TestFullNameGenerator(TestCase):
    def setUp(self):
        self.first_names = ['joe', 'jim', 'jane']
        self.last_names = ['smith', 'johnson', 'williams']

    def test_full_name_generator(self):
        g = FullNameGenerator(
                first_names=self.first_names,
                last_names=self.last_names,
                )
        self.assertEqual(len(g), 9)


class TestTitleGenerator(TestCase):
    def test_base_title_generator(self):
        g = TitleGenerator()
        for i, title in enumerate(g):
            if i > 20:
                break
            self.assertTrue(len(title) >= g.min_length, "{0} is not greater than {1}".format(len(title), g.min_length))
            self.assertTrue(len(title) <= g.max_length, "{0} is not less than {1}".format(len(title), g.min_length))
