from __future__ import division
import random
import datetime

from perjury.generators.base import BaseGenerator


def total_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def datetime_in_range(start_at, end_at):
    """
    Generates a random datetime between start and end datetime values.
    """
    td = end_at - start_at
    seconds = int(total_seconds(td))
    return start_at + datetime.timedelta(seconds=random.randrange(seconds))


class DatetimeGenerator(BaseGenerator):
    """
    Class-based generator for generating random datetime values.
    """
    unique = False

    def start_at(self):
        return datetime.datetime.min

    def end_at(self):
        return datetime.datetime.max

    def generator(self):
        return datetime_in_range(self.start_at(), self.end_at())
