from perjury.generators.base import BaseResource, FormattedStringResource
from perjury.content import (
    DOMAIN_NAMES, USERNAMES,
)


username = BaseResource(USERNAMES)


class EmailAddressResource(FormattedStringResource):
    template = '{username}@{domain}'

email_address = EmailAddressResource(
    username=BaseResource(USERNAMES),
    domain=BaseResource(DOMAIN_NAMES),

)
