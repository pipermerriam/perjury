import unittest

from perjury.generators.base import BaseResource


class BaseResourceTest(unittest.TestCase):
    def test_calling(self):
        numbers = [1, 2, 3, 4]
        generator = BaseResource(numbers)

        self.assertEqual(generator(), 1)
        self.assertEqual(generator(), 2)
        self.assertEqual(generator(), 3)
        self.assertEqual(generator(), 4)
        with self.assertRaises(StopIteration):
            generator()

    def test_iteration(self):
        values = ['a', 'b', 'c']
        generator = BaseResource(values)

        result = [v for v in generator]
        self.assertSequenceEqual(values, result)
