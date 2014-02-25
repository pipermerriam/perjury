import unittest

from perjury.utils import ResourceCheckMixin


class FirstNameResourceCheck(ResourceCheckMixin, unittest.TestCase):
    resource_path = 'perjury.generators.people.first_name'
