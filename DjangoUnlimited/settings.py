"""
Django settings for DjangoUnlimited project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import urllib

from django.conf.locale.en import formats as en_formats
from django.contrib import messages
from dotenv import load_dotenv

# from .api_key import SENDGRID_API_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

FORMAT_MODULE_PATH = 'DjangoUnlimited.formats'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv('.env')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p-y$&3u8l04=z-*r#2t&+ff2#&c2)+6$$tmpqf#vo8s3n57dxt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', '127.0.0.1']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django_comments',
    'django.contrib.sites',
    'django_cleanup',
    'django.contrib.staticfiles',
    'django_countries',
    'rest_framework',
    'django.contrib.humanize',
    'rest_framework_datatables',
    'widget_tweaks',
    'dbbackup_ui',
    'datatableview',
    'mathfilters',
    'phonenumber_field',
    'crispy_forms',
    'Student',
    'Employer',
    'Admin',
    'Home',
    'HelpDesk',
    'Accounts',
    'Alumni',
    'Bulletin',
    'boto',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = False
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

JOB_ID = os.getenv("JOB_ID")

SITE_ID = 1  # needed for 'django.contrib.sites' to work for admin site

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoUnlimited.urls'

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

WSGI_APPLICATION = 'DjangoUnlimited.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_unlimited',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'Django-Unlimited',
#         'USER': 'postgres',
#         'PASSWORD': '1234',
#         'HOST': 'localhost',
#         'PORT': '5432',
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

TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# Sets a location to where the static files are supposed to be.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# STATIC_ROOT = 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Sets a location to where the media files are supposed to be.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_PERMISSIONS = 0o644

BACKUP_URL = '/backup/'
BACKUP_ROOT = os.path.join(BASE_DIR, 'backup')

LOGIN_URL = 'log_in'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'log_in'

# URLS that are allowed to access the Intranet without the need to login.
LOGIN_EXEMPT_URLS = {
    'accounts/login',
    'password_reset/',
    'reset/',
    'media/'
}

# Date input format.
DATE_INPUT_FORMATS = ['%d/%m/%Y']

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}
