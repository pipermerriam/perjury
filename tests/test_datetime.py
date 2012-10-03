import datetime

from unittest import TestCase

from perjury.generators.datetime_generators import datetime_in_range
from perjury.generators import datetime_generator, current_datetime


class DatetimeGeneratorTest(TestCase):
    def test_date_in_range_func_generation(self):
        for i in xrange(1000):
            week_ago = datetime.datetime.now() - datetime.timedelta(7)
            week_away = datetime.datetime.now() + datetime.timedelta(7)
            value = datetime_in_range(week_ago, week_away)
            self.assertTrue(value <= week_away)
            self.assertTrue(value >= week_ago)

    def test_generator_function(self):
        for i in xrange(1000):
            value = datetime_generator()
            self.assertTrue(value <= datetime.datetime.max)
            self.assertTrue(value >= datetime.datetime.min)

    def test_current_generator(self):
        for i in xrange(1000):
            td = current_datetime() - datetime.datetime.now()
            one_month = datetime.timedelta(30)

            self.assertTrue(td <= one_month)
