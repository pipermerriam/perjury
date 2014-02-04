import unittest

from perjury.generators.base import SimpleResource


class SimpleResourceTest(unittest.TestCase):
    def test_calling(self):
        numbers = [1, 2, 3, 4]
        generator = SimpleResource(numbers)

        self.assertEqual(generator(), 1)
        self.assertEqual(generator(), 2)
        self.assertEqual(generator(), 3)
        self.assertEqual(generator(), 4)
        with self.assertRaises(StopIteration):
            generator()

    def test_iteration(self):
        values = ['a', 'b', 'c']
        generator = SimpleResource(values)

        result = [v for v in generator]
        self.assertSequenceEqual(values, result)

    def test_multiplication(self):
        values = ['a', 'b', 'c', 'd']
        generator = SimpleResource(values)
        result = generator * 3
        self.assertSequenceEqual(['a', 'b', 'c'], result)
