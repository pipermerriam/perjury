from perjury.generators.base import BaseResource, FormattedStringResource
from perjury.content import (
    MALE_NAMES, FEMALE_NAMES, FIRST_NAMES, LAST_NAMES,
)


male_first_name = BaseResource(MALE_NAMES)
female_first_name = BaseResource(FEMALE_NAMES)

first_name = BaseResource(FIRST_NAMES)
last_name = BaseResource(LAST_NAMES)


class FullNameResource(FormattedStringResource):
    template = '{first_name} {last_name}'


full_name = FullNameResource(
    first_name=BaseResource(FIRST_NAMES),
    last_name=BaseResource(LAST_NAMES),
)
