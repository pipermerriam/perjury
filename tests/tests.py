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

    def test_base_name_generator_custom_length(self):
        class BasicWordGenerator(WordGenerator):
            shuffle = False
            words = self.names
        g = BasicWordGenerator()
        names = [g.next() for i in range(2)]
        self.assertEqual(names, self.names[:2])

    def test_name_generator_classes(self):
        for NameGeneratorClass in [FirstNameGenerator, MaleNameGenerator,
                FemaleNameGenerator, LastNameGenerator]:
            g = NameGeneratorClass()
            self.do_assertions(g)

    def do_assertions(self, generator):
        for i in range(100):
            name = generator.next()
            self.assertIn(name, generator.words)


class TestRepeatValueGenerator(unittest.TestCase):
    def test_returns_same_value(self):
        g = RepeatValueGenerator(value='arst')
        for i in range(20):
            self.assertEqual(g.next(), 'arst')


class TestSingleLineTextGenerator(unittest.TestCase):
    def test_single_line_text_generator(self):
        g = SingleLineTextGenerator()
        for i in range(100):
            line = g.next()
            self.assertTrue(len(line) >= g.min_length, "{0} is not greater than {1}".format(len(line), g.min_length))
            self.assertTrue(len(line) <= g.max_length, "{0} is not less than {1}".format(len(line), g.min_length))


class TestTitleGenerator(unittest.TestCase):
    def test_base_title_generator(self):
        g = TitleGenerator()
        for i in range(100):
            title = g.next()
            self.assertEqual(title[0].upper(), title[0])
            self.assertEqual(title[1:].lower(), title[1:])


class IntegerGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = RandomIntegerGenerator()
        for i in range(100):
            i = g.next()
            self.assertGreaterEqual(i, g.lower_bound)
            self.assertLessEqual(i, g.upper_bound)

    def test_ordered_generator(self):
        class TestGenerator(OrderedIntegerGenerator):
            lower_bound = 0
            upper_bound = 20

        g = TestGenerator()
        for i in range(100):
            j = g.next()
            self.assertEqual(i % 20, j)


class TrueGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = TrueGenerator()
        self.assertTrue(all([g.next() for i in range(20)]))


class FalseGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = FalseGenerator()
        self.assertTrue(all([not g.next() for i in range(20)]))


class BooleanGeneratorTest(unittest.TestCase):
    def test_basic_generator(self):
        g = RandomBooleanGenerator()
        self.assertTrue(all([g.next() in g.values for i in range(20)]))


class GmailAddressGeneratorTest(unittest.TestCase):
    is_gmail_address = re.compile(r'^[_.0-9a-z-]+@gmail\.com$')

    def test_basic_generator(self):
        g = GmailAddressGenerator()
        for e in range(20):
            self.assertTrue(self.is_gmail_address.match(g.next()))


if __name__ == '__main__':
        unittest.main()
