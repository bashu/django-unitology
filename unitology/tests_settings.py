# Settings to be used when running unit tests
# python manage.py test --settings=unitology.test_settings unitology

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'tests.sqlite'),
    }
}

SITE_ID = 1

STATIC_URL = '/site_media/static/'

ROOT_URLCONF = 'unitology.tests_urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # local
    'unitology',
)
