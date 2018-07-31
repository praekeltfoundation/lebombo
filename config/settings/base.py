import environ

from os.path import join
from django.conf import global_settings
from django.conf.locale import LANG_INFO
from django.utils.translation import ugettext_lazy as _

root = environ.Path(__file__) - 3
env = environ.Env(DEBUG=(bool, False))

ROOT_DIR = root()
environ.Env.read_env(join(ROOT_DIR, ".env"))

ALLOWED_HOSTS = []

DJANGO_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
)

THIRD_PARTY_APPS = ()

LOCAL_APPS = ("lebombo",)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE", "en")
TIME_ZONE = "Africa/Johannesburg"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = global_settings.LANGUAGES + [
    ("zu", _("Zulu")),
    ("xh", _("Xhosa")),
    ("st", _("Sotho")),
    ("ve", _("Venda")),
    ("tn", _("Tswana")),
    ("ts", _("Tsonga")),
    ("ss", _("Swati")),
    ("nr", _("Ndebele")),
]

EXTRA_LANG_INFO = {
    "zu": {"bidi": False, "code": "zu", "name": "Zulu", "name_local": "isiZulu"},
    "xh": {"bidi": False, "code": "xh", "name": "Xhosa", "name_local": "isiXhosa"},
    "st": {"bidi": False, "code": "st", "name": "Sotho", "name_local": "seSotho"},
    "ve": {"bidi": False, "code": "ve", "name": "Venda", "name_local": u"tshiVenḓa"},
    "tn": {"bidi": False, "code": "tn", "name": "Tswana", "name_local": "Setswana"},
    "ts": {"bidi": False, "code": "ts", "name": "Tsonga", "name_local": "xiTsonga"},
    "ss": {"bidi": False, "code": "ss", "name": "Swati", "name_local": "siSwati"},
    "nr": {"bidi": False, "code": "nr", "name": "Ndebele", "name_local": "isiNdebele"},
}

LANG_INFO.update(EXTRA_LANG_INFO)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = join(ROOT_DIR, "static")
STATIC_URL = "/static/"
COMPRESS_ENABLED = True
MEDIA_ROOT = join(ROOT_DIR, "media")
MEDIA_URL = "/media/"
