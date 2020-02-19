"""
Django settings for cdsimgs2t project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import configparser
# Tricky lib to convert string to boolean directly in python.
from distutils.util import strtobool

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Get Environment Variables from .env
my_env = os.environ.copy()
parser = configparser.ConfigParser({k: v.replace('$', '$$') for k, v in os.environ.items()},
         interpolation=configparser.ExtendedInterpolation())
settingsFile = os.path.join(BASE_DIR, ".env")
if os.path.isfile(settingsFile):
    with open(settingsFile) as stream:
        parser.read_file(['[DEFAULT]\n', *stream])
        for k, v in parser["DEFAULT"].items():
            my_env.setdefault(k.upper(), v)

# Environment Variables Import
try:
    # Amazon s3 secret
    AWS_ACCESS_KEY_ID = my_env['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = my_env['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = my_env['AWS_STORAGE_BUCKET_NAME']
    IS_PRODUCTION_SITE = strtobool(my_env['IS_PRODUCTION_SITE'])
    TEST_HTTP_HANDLING = strtobool(my_env.get('TEST_HTTP_HANDLING', 'False'))
    IS_GOOGLE_CLOUD = strtobool(my_env.get('IS_GOOGLE_CLOUD', 'False'))
    NUMROUNDS = {
        'phase01a': int(my_env.get('NUMROUNDS_STEP1', my_env.get('NUMROUNDS', '5'))), # step 1
        'phase01b': int(my_env.get('NUMROUNDS_STEP2', '5')), # step 2
        'phase03': 1 # step 3
    }

    # Local development
    if not IS_PRODUCTION_SITE:
        print('Local development')
        # Set up database url
        DATABASE_URL = my_env.get('DATABASE_URL', None) or (
            'postgres://cam2dev:%s@cdstest-s20.cpvnurwrwbko.us-east-1.rds.amazonaws.com:5432/postgres'
            % (my_env['POSTGRESQLPASS'],))
        # Database
        # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
        import dj_database_url
        DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600, ssl_require=True)}
    else:
        print("Production site")
        DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ['DB_PORT'],
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD']
        }
    }

    # Environment variable for set up the object we are going to use. By default we set to airplanes
    OBJECT_NAME_PLURAL = my_env.get('KEY', 'People')
    # KEYRING = KEY.rsplit('/', 1)[0]+'/'
    # OBJECT_NAME_PLURAL = my_env.get('OBJECT_NAME_PLURAL', KEY.split('/')[1]+'s')

except KeyError as e:
    exit('Lacking Environment Variables: ' + str(e)) # indicate to the OS that the program has failed

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u)cteee4ggd#ce72t!xn-wzhll5%#$w6$4akiag0(=*2*-rfmy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'cmpUI.apps.CmpuiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Ask Xiao what is this
if os.environ['ENABLE_LIVERELOAD']:
    # INSTALLED_APPS.insert(0, "'livereload',") # has to be before staticfiles
    INSTALLED_APPS.append("livereload")
    MIDDLEWARE.append("'livereload.middleware.LiveReloadScript',")

ROOT_URLCONF = 'cdsimgs2t.urls'

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

WSGI_APPLICATION = 'cdsimgs2t.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = my_env.get('STATIC_URL', '/static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

if not IS_PRODUCTION_SITE:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'cds-s20-static')


# File upload
MEDIA_URL = '/data/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'data')
DATA_UPLOAD_MAX_MEMORY_SIZE = 1073741824

#Default file storage
DEFAULT_FILE_STORAGE = 'cdsimgs2t.storage_backends.MediaStorage'

# Cloud Service by amazon s-3
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = None
