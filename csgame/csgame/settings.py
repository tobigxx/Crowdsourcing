"""
Django settings for csgame project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import configparser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR =  os.path.dirname(PROJECT_ROOT)


# Get Environment Variables from .env
my_env = os.environ.copy()
parser = configparser.ConfigParser({k: v.replace('$', '$$') for k, v in os.environ.items()},
         interpolation=configparser.ExtendedInterpolation())
def defaultSect(fp): yield '[DEFAULT]\n'; yield from fp
settingsFile = os.path.join(BASE_DIR, ".env")
if os.path.isfile(settingsFile):
    with open(settingsFile) as stream:
        parser.read_file(defaultSect(stream))
        for k, v in parser["DEFAULT"].items():
            my_env.setdefault(k.upper(), v)

# Environment Variables Import
try:
    # Amazon s3 secret
    AWS_ACCESS_KEY_ID = my_env['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = my_env['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = my_env['AWS_STORAGE_BUCKET_NAME']
    IS_PRODUCTION_SITE = my_env['IS_PRODUCTION_SITE']
    TEST_HTTP_HANDLING = my_env['TEST_HTTP_HANDLING']

except KeyError as e:
    print('Lacking Environment Variables: ' + str(e))
    exit()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jsl5xrm^in$mx)ftkdeybi0#(uqr)j=e=eer%eg2rxk#h#1l9r'

# SECURITY WARNING: don't run with debug turned on in production!
if IS_PRODUCTION_SITE or TEST_HTTP_HANDLING:
    DEBUG=False
else:
    DEBUG=True

DEBUG=True
ALLOWED_HOSTS = [
	'cdstrain.herokuapp.com',
    '127.0.0.1'	
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'corsheaders',
    'rest_framework',
    'storages'
]

MIDDLEWARE = [
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'csgame.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'csgame.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

in_heroku = False
if 'DATABASE_URL' in os.environ:
    in_heroku = True

import dj_database_url
if in_heroku:
    DATABASES = {'default': dj_database_url.config()}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'users.CustomUser'

LOGIN_URL='login'

LOGOUT_URL='logout'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'home'

# Cloud Service by amazon s-3
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = None

# File upload ?
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#Default file storage
DEFAULT_FILE_STORAGE = 'csgame.storage_backends.MediaStorage'