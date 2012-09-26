import unittest
import re

from foundry.generators import (WordGenerator, FirstNameGenerator,
        MaleNameGenerator, FemaleNameGenerator, LastNameGenerator,
        FullNameGenerator, SingleLineTextGenerator, TitleGenerator,
        RepeatValueGenerator, RandomIntegerGenerator, OrderedIntegerGenerator,
        TrueGenerator, FalseGenerator, RandomBooleanGenerator,
        GmailAddressGenerator)


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
            shuffle = False
            words = self.names
        g = BasicWordGenerator()
        names = g[1:3]
        self.assertEqual(names, self.names[1:3])

    def test_base_name_generator_custom_length(self):
        class BasicWordGenerator(WordGenerator):
            shuffle = False
            words = self.names
        g = BasicWordGenerator(2)
        self.assertEqual(len(g), 2)
        names = [name for name in g]
        self.assertEqual(len(names), 2)
        self.assertEqual(names, self.names[:2])

    def test_name_generator_classes(self):
        for NameGeneratorClass in [FirstNameGenerator, MaleNameGenerator,
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


class IntegerGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = RandomIntegerGenerator(100)
        for i in g:
            self.assertGreaterEqual(i, g.lower_bound)
            self.assertLess(i, g.upper_bound)

    def test_ordered_generator(self):
        class TestGenerator(OrderedIntegerGenerator):
            lower_bound = 0
            upper_bound = 20

        g = TestGenerator(100)
        for i, j in enumerate(g):
            self.assertEqual(i % 20, j)


class TrueGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = TrueGenerator(20)
        self.assertTrue(all([val for val in g]))


class FalseGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = FalseGenerator(20)
        self.assertTrue(all([not val for val in g]))


class BooleanGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = RandomBooleanGenerator(20)
        self.assertTrue(all([val in g.values for val in g]))


class GmailAddressGeneratorTest(unittest.TestCase):
    is_gmail_address = re.compile(r'^[_.0-9a-z-]+@gmail\.com$')

    def test_basic_generator(self):
        g = GmailAddressGenerator(20)
        for e in g:
            self.assertTrue(re.match(e))


if __name__ == '__main__':
        unittest.main()
