from perjury.generators.base import SimpleResource, FormattedStringResource
from perjury.content import (
    MALE_NAMES, FEMALE_NAMES, FIRST_NAMES, LAST_NAMES,
)


male_first_name = SimpleResource(MALE_NAMES)
female_first_name = SimpleResource(FEMALE_NAMES)

first_name = SimpleResource(FIRST_NAMES)
last_name = SimpleResource(LAST_NAMES)


class FullNameResource(FormattedStringResource):
    template = '{first_name} {last_name}'


full_name = FullNameResource(
    first_name=SimpleResource(FIRST_NAMES),
    last_name=SimpleResource(LAST_NAMES),
)
