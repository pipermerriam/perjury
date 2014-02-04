from perjury.generators.base import SimpleResource, FormattedStringResource
from perjury.content import (
    DOMAIN_NAMES, USERNAMES,
)


username = SimpleResource(USERNAMES)


class EmailAddressResource(FormattedStringResource):
    template = '{username}@{domain}'

email_address = EmailAddressResource(
    username=SimpleResource(USERNAMES),
    domain=SimpleResource(DOMAIN_NAMES),

)
