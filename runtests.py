import os
import unittest

BASE_DIR = os.path.dirname(__file__)


def main():
    run_unittests()


def run_unittests():
    loader = unittest.TestLoader()
    suite = loader.discover(BASE_DIR)
    result = suite.run(unittest.TestResult())

    if result.wasSuccessful():
        print 'Success'
    else:
        print 'Failed'
        result.printErrors()


if __name__ == '__main__':
    main()
