from .base import *
from .dbconf import POSTGRESDB, MANGODB

"""Production Ready Settings
"""

TEMP_SECRET_KEY = "srt@v69cp$hm2^g-z#m%n18pl(+*mmx6+tl$t^s9h55%1v%*it"
SECRET_KEY = os.environ.get("SECRET_KEY", TEMP_SECRET_KEY)
DEBUG = False

ALLOWED_HOSTS += [
    "central.kedco.ng",
    "www.central.kedco.ng",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

DATABASES = POSTGRESDB
# DATABASES = MANGODB


STATIC_ROOT = os.path.join(PROJECT_ROOT, "staticfiles")
STATIC_URL = "/kedco_centralstatic/"
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (os.path.join(PROJECT_ROOT, "static"),)
MEDIA_URL = "/kedco_centralmedia/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
