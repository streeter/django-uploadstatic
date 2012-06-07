import os

SITE_ID = 1

TEST_ROOT = os.path.join(os.path.normcase(os.path.dirname(os.path.abspath(__file__))), 'tests')

DATABASE_ENGINE = 'sqlite3'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(TEST_ROOT, 'project', 'site_media', 'media')

ADMIN_MEDIA_PREFIX = '/static/admin/'

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(TEST_ROOT, 'project', 'site_media', 'static')

ROOT_URLCONF = 'uploadstatic.tests.urls.default'

TEMPLATE_DIRS = (
    os.path.join(TEST_ROOT, 'project', 'templates'),
)

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.admin',
    'uploadstatic',
    'uploadstatic.tests',
    'uploadstatic.tests.apps.test',
]

TEST_RUNNER = 'discover_runner.DiscoverRunner'
