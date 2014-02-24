from unittest import TestCase
import random

from perjury.generators import BaseGenerator, sequence, consumer


class TestBasicBaseGenerator(TestCase):
    def setUp(self):
        class TestGenerator(BaseGenerator):
            def generator(self):
                i = 0
                while True:
                    yield i
                    i += 1
        self.generator_class = TestGenerator

    def test_callable_generation(self):
        generator = self.generator_class()
        while True:
            if generator() > 20:
                break


class TestGeneratorUniqueness(TestCase):
    def setUp(self):
        class TestGenerator(BaseGenerator):
            def generator(self):
                while True:
                    yield random.randint(0, 1000)
        self.generator_class = TestGenerator

    def test_unique_values(self):
        generator = self.generator_class()
        values = set()
        for i in range(1000):
            value = generator()
            assert value not in values
            values.add(value)


class TestConsumer(TestCase):
    def test_consumer(self):
        generator = consumer([1, 2, 3])
        self.assertEqual(generator(), 1)
        self.assertEqual(generator(), 2)
        self.assertEqual(generator(), 3)

    def test_consumer_error(self):
        generator = consumer([1])
        self.assertEqual(generator(), 1)

        self.assertRaises(StopIteration, generator)


class TestSequence(TestCase):
    def test_sequence(self):
        generator = consumer(sequence())
        self.assertEqual(generator(), 1)
        self.assertEqual(generator(), 2)
        self.assertEqual(generator(), 3)
        self.assertEqual(generator(), 4)
        self.assertEqual(generator(), 5)
        self.assertEqual(generator(), 6)

    def test_sequence_start(self):
        generator = consumer(sequence(start=5))
        self.assertEqual(generator(), 5)
        self.assertEqual(generator(), 6)
        self.assertEqual(generator(), 7)
        self.assertEqual(generator(), 8)

    def test_sequence_incr(self):
        generator = consumer(sequence(start=5, incr=-5))
        self.assertEqual(generator(), 5)
        self.assertEqual(generator(), 0)
        self.assertEqual(generator(), -5)


#class TestDecimalGenerator(TestCase):
#    def setUp(self):
#        class TestGenerator(DecimalGenerator):
#            upper_bound = 10
#            lower_bound = 0
#            precision = 5
#        self.generator_class = TestGenerator
#
#    def test_in_bounds(self):
#        generator = self.generator_class()
#        for i in range(100):
#            d = generator()
#            self.assertLessEqual(d, self.generator_class.upper_bound)
#            self.assertGreaterEqual(d, self.generator_class.lower_bound)
#
#    def test_precision(self):
#        generator = self.generator_class()
#        t = Decimal(("0.{0:0" + str(generator.precision) + "}").format(0))
#        for i in range(100):
#            d = generator()
#            self.assertEqual(d, d.quantize(t))
