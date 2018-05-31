from .base import *
from .base import env

from os.path import join
import dj_database_url


DEBUG = env.bool("DJANGO_DEBUG", True)

SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="^92l&5_l2f-ik5xlav!7*cat904fro-lmdd@0kgz@c*nxua3@p"
)

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", False).split(",") + (
    "localhost", ".localhost", "127.0.0.1"
)

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///{}".format(join(ROOT_DIR, "db.sqlite3"))
    )
}
