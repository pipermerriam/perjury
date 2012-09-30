from django.conf import settings

# https://docs.djangoproject.com/en/dev/topics/settings/#using-settings-without-setting-django-settings-module
settings.configure(
        DEBUG=True,
        )

import test_django
