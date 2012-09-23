import unittest

from pyrite.generators import (WordGenerator, NameGenerator,
        MaleNameGenerator, FemaleNameGenerator, LastNameGenerator,
        FullNameGenerator, SingleLineTextGenerator, TitleGenerator,
        RepeatValueGenerator)


class TestNameGenerators(unittest.TestCase):
    def setUp(self):
        self.names = ['joe', 'jim', 'john']

    def test_base_name_generator(self):
        class BasicWordGenerator(WordGenerator):
            words = self.names
        g = BasicWordGenerator()
        self.assertEqual(len(g), 3)

    def test_base_name_generator_slicing(self):
        class BasicWordGenerator(WordGenerator):
            words = self.names
        g = BasicWordGenerator()
        names = g[1:3]
        self.assertEqual(names, self.names[1:3])

    def test_base_name_generator_custom_length(self):
        class BasicWordGenerator(WordGenerator):
            words = self.names
        g = BasicWordGenerator(2)
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
        self.assertEqual(len(generator), len(generator.words))
        for name in generator:
            self.assertIn(name, generator.words)


class TestFullNameGenerator(unittest.TestCase):
    def setUp(self):
        self.first_names = ['joe', 'jim', 'jane']
        self.last_names = ['smith', 'johnson', 'williams']

    def test_full_name_generator(self):
        class TestFullNameGenerator(FullNameGenerator):
            first_names = self.first_names
            last_names = self.last_names
        g = TestFullNameGenerator()
        self.assertEqual(len(g), 9)

    def test_large_iteration_count(self):
        g = FullNameGenerator(5000)
        for name in g:
            pass


class TestRepeatValueGenerator(unittest.TestCase):
    def test_returns_same_value(self):
        class TestRepeatValueGenerator(RepeatValueGenerator):
            value = 'arstarst'
        g = TestRepeatValueGenerator(20)
        for i, value in enumerate(g):
            self.assertEqual(value, 'arstarst')
        self.assertEqual(i, 19)


class TestSingleLineTextGenerator(unittest.TestCase):
    def test_single_line_text_generator(self):
        g = SingleLineTextGenerator(100)
        for line in g:
            self.assertTrue(len(line) >= g.min_length, "{0} is not greater than {1}".format(len(line), g.min_length))
            self.assertTrue(len(line) <= g.max_length, "{0} is not less than {1}".format(len(line), g.min_length))


class TestTitleGenerator(unittest.TestCase):
    def test_base_title_generator(self):
        g = TitleGenerator(100)
        for title in g:
            self.assertEqual(title[0].upper(), title[0])
            self.assertEqual(title[1:].lower(), title[1:])

if __name__ == '__main__':
        unittest.main()
