import random
import datetime
from perjury.generators.base import BaseResource


class BaseDatetimeResource(BaseResource):
    def __init__(self, back_drift, forward_drift):
        self.back_drift = back_drift
        self.forward_drift = forward_drift

    @property
    def generator(self):
        while True:
            anchor = datetime.datetime.now() - self.back_drift
            range_seconds = (
                self.back_drift.total_seconds() + self.forward_drift.total_seconds()
            )
            delta = datetime.timedelta(seconds=random.randint(range_seconds))
            yield anchor + delta


last_day = BaseDatetimeResource(
    back_drift=datetime.timedelta(1),
    forward_drift=datetime.timedelta(0),
)
last_week = BaseDatetimeResource(
    back_drift=datetime.timedelta(7),
    forward_drift=datetime.timedelta(0),
)
last_month = BaseDatetimeResource(
    back_drift=datetime.timedelta(30),
    forward_drift=datetime.timedelta(0),
)
last_year = BaseDatetimeResource(
    back_drift=datetime.timedelta(365),
    forward_drift=datetime.timedelta(0),
)

next_day = BaseDatetimeResource(
    back_drift=datetime.timedelta(0),
    forward_drift=datetime.timedelta(1),
)
next_week = BaseDatetimeResource(
    back_drift=datetime.timedelta(0),
    forward_drift=datetime.timedelta(7),
)
next_month = BaseDatetimeResource(
    back_drift=datetime.timedelta(0),
    forward_drift=datetime.timedelta(30),
)
next_year = BaseDatetimeResource(
    back_drift=datetime.timedelta(0),
    forward_drift=datetime.timedelta(365),
)
