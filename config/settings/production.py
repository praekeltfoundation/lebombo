from .base import *  # noqa
from .base import env


DEBUG = False

# Raises ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS").split(",")

# Configure Sentry Logging
INSTALLED_APPS += ("raven.contrib.django.raven_compat",)
RAVEN_DSN = env.str("RAVEN_DSN", False)
RAVEN_CONFIG = {"dsn": RAVEN_DSN} if RAVEN_DSN else {}

DATABASES = {
    "default": env.db(
        var="DATABASE_URL",
        default="postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(
            **{
                "USER": env.str("DB_USER", "lebombo"),
                "PASSWORD": env.str("DB_PASSWORD", "lebombo"),
                "HOST": env.str("DB_HOST", "localhost"),
                "PORT": env.str("DB_PORT", ""),
                "NAME": env.str("DB_NAME", "lebombo"),
            }
        ),
    )
}

RAPIDPRO_API_KEY = env.str("RAPIDPRO_API_KEY")
