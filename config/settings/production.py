from .base import *

import environ

from django.core.exceptions import ImproperlyConfigured


DEBUG = False

# configure Sentry Logging
INSTALLED_APPS += ("raven.contrib.django.raven_compat")
RAVEN_DSN = environ.get("RAVEN_DSN")
RAVEN_CONFIG = {"dsn": RAVEN_DSN} if RAVEN_DSN else {}

if SECRET_KEY == DEFAULT_SECRET_KEY:  # noqa: F405
    raise ImproperlyConfigured("SECRET_KEY is set to default value")

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
            {
                "NAME": "postgres",
                "HOST": "postgres",
                "USER": "db",
                "PASSWORD": "postgres",
                "PORT": 5432,
            }
        )
    )
}

MEDIA_ROOT = join(PROJECT_ROOT, "media")

STATIC_ROOT = join(PROJECT_ROOT, "static")
