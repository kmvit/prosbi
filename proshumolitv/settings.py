"""
Django settings for proshumolitv project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from datetime import timedelta
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jxu^1)9cn+llgx7i9!=1i8x&6&!qxe2e!$q6m8b$j$=(ri19-m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['forum.findotvet.ru']



EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = 'dronich26rus@mail.ru'
EMAIL_HOST_PASSWORD = 'justscoundrel'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'dronich26rus@mail.ru'
SERVER_EMAIL = 'dronich26rus@mail.ru'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_markdown',
    'south',
    'djcelery',
    'kombu.transport.django',
    'mymenu',
    'names',
    'prays',
    'legends',
    'icons',

    'account',
    'requests',
    'reminders',
    'pages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proshumolitv.urls'

WSGI_APPLICATION = 'proshumolitv.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = { 'default': { 'ENGINE': 'django.db.backends.mysql', 'NAME' : 'justscoundrel_prosbi',
                           'USER': 'justscoundrel', 'PASSWORD': 'urha-murha',
                           'HOST': '127.0.0.1', 'PORT': '',
                           'OPTIONS': { 'init_command': 'SET storage_engine=MYISAM;' }
                             } }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT =  os.path.join(BASE_DIR, 'static')

STATIC_URL =  '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'


MEDIA_ROOT='/home/users1/j/justscoundrel/domains/forum.findotvet.ru/media/'
MEDIA_URL =  '/media/'

TEMPLATE_DIRS=('/home/users1/j/justscoundrel/django/proshumolitv/templates/',)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]



TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'mymenu.context_processors.context',
)

SESSION_SAVE_EVERY_REQUEST = True

# Celery settings

BROKER_URL = 'django://'
CELERY_TIMEZONE = TIME_ZONE
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'




# ADMINS SEND MAIL


ADMINS = (('Administrator', 'justscoundrel@yandex.ru'),)


REQUESTS_ON_PAGE = 10