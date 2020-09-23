"""
With these settings, tests run faster.
"""
import os

from .base import *  # noqa

INSTALLED_APPS += ['django_nose',]
# https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# TEST_RUNNER = "django.test.runner.DiscoverRunner"

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    default="kY2h68D0TgYGFibh1GiRlZ1PLE52zTKpbIFIymEsNc5zoauSn6asnnSr2dtOiOf1",
)

NOSE_ARGS = [
    APPS_DIR,
    '-s',
    '--nologcapture',
    '--with-coverage',
    '--with-progressive',
    '--cover-package=yadrta'
]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(ROOT_DIR, "db.sqlite3"),
    }
}
