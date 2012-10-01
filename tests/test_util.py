from unittest import TestCase

from perjury import generators as g
from perjury import util
from perjury.exceptions import UniqueValueTimeoutError


class TestUniqueDecorator(TestCase):
    def test_is_pretty_unique(self):
        # This is not the most scientific way to test it, but we have slightly
        # more than 400 usernames, if we generate 400 unique usernames 1000
        # times, it is probably likely that this works.
        for i in xrange(1000):
            unique_username = util.unique(g.username)

            seen = set()
            for i in xrange(400):
                username = unique_username()
                self.assertNotIn(username, seen)
                seen.add(username)

    def test_overflow(self):
        generator = util.unique(g.Choice(choices=(1, 2, 3)))

        generator()
        generator()
        generator()

        with self.assertRaises(UniqueValueTimeoutError):
            generator()


class TestIterableUtils(TestCase):
    def test_forever(self):
        forever_usernames = util.forever(g.username)

        count = 0
        for username in forever_usernames:
            count += 1

            # 100,000 is basically forever right?
            if count > 100000:
                break

    def test_times(self):
        three_usernames = util.times(g.username, 3)

        count = 0
        for username in three_usernames:
            count += 1

        assert count == 3

    def test_composability(self):
        for i in xrange(1000):
            unique_usernames = util.unique(g.username)
            many_unique_usernames = util.times(unique_usernames, 400)

            seen = set()
            count = 0
            for username in many_unique_usernames:
                count += 1
                self.assertNotIn(username, seen)
                seen.add(username)

            assert count == 400
