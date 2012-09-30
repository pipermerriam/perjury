import unittest
import random
from decimal import Decimal

from foundry.base import BaseGenerator, DecimalGenerator
from foundry.exceptions import UniqueValueTimeoutError


class TestBasicBaseGenerator(unittest.TestCase):
    def setUp(self):
        class TestGenerator(BaseGenerator):
            def generator(self):
                i = 0
                while True:
                    yield i
                    i += 1
        self.generator_class = TestGenerator

    def test_callable_generation(self):
        g = self.generator_class()
        while True:
            if g() > 20:
                break

    def test_iterable_generation(self):
        g = self.generator_class()
        for i in g:
            if i > 20:
                break

    def test_next_generation(self):
        g = self.generator_class()
        while True:
            if g.next() > 20:
                break

    def test_reset(self):
        g = self.generator_class()
        for i in range(20):
            g.next()

        self.assertEqual(g.next(), 20)
        g.reset()
        self.assertEqual(g.next(), 0)


class TestGeneratorUniqueness(unittest.TestCase):
    def setUp(self):
        class TestGenerator(BaseGenerator):
            def generator(self):
                while True:
                    yield random.randint(0, 1000)
        self.generator_class = TestGenerator

    def test_unique_values(self):
        g = self.generator_class()
        values = set()
        for i in range(1000):
            value = g.next()
            self.assertNotIn(value, values)
            values.add(value)


class TestUniqueTimeout(unittest.TestCase):
    def setUp(self):
        class TestGenerator(BaseGenerator):
            def generator(self):
                while True:
                    yield random.randint(0, 1000000)
        self.generator_class = TestGenerator

    @unittest.skip('Test takes far too long to run')
    def test_timeout(self):
        """
        This test takes a while to run.  What is a better way to do this.
        """
        g = self.generator_class()
        with self.assertRaises(UniqueValueTimeoutError):
            for i in range(1000000):
                g.next()


class TestDecimalGenerator(unittest.TestCase):
    def setUp(self):
        class TestGenerator(DecimalGenerator):
            upper_bound = 10
            lower_bound = 0
            precision = 5
        self.generator_class = TestGenerator

    def test_in_bounds(self):
        g = self.generator_class()
        for i in range(100):
            d = g()
            self.assertLessEqual(d, self.generator_class.upper_bound)
            self.assertGreaterEqual(d, self.generator_class.lower_bound)

    def test_precision(self):
        g = self.generator_class()
        t = Decimal(("0.{0:0" + str(g.precision) + "}").format(0))
        for i in range(100):
            d = g()
            self.assertEqual(d, d.quantize(t))


if __name__ == '__main__':
    unittest.main()
