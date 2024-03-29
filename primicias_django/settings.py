"""
Django settings for tutorial project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from django.core import serializers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# with open(os.path.join(BASE_DIR, 'tutorial/secret_key.txt')) as archivo:
#    SECRET_KEY = archivo.read().strip()
SECRET_KEY = 'f&j_4!@utn@eehwg+s7bg1(ju7q@wir#r9!-3xqr3tf*14v8p_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True) )

ALLOWED_HOSTS = ['www.primicias.com.py']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'tutorial.GestionUsuarios',
    'tutorial.GestionClientes',
    'tutorial.GestionSistema',
    'tutorial.GestionRolesyPermisos',
    'tutorial.GestionPlatos',
    'tutorial.GestionMenu',
    'tutorial.GestionPedidos',
    'tutorial.GestionDelivery',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tutorial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'tutorial/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

# TEMPLATE_DEBUG = True

# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

WSGI_APPLICATION = 'tutorial.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
with open(os.path.join(BASE_DIR, 'tutorial/bd_parametros.txt')) as archivo:
    contrasenha = archivo.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tutorial',
        'USER': 'postgres',
        'PASSWORD': contrasenha,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimila'
        'rityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLength'
        'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPassword'
        'Validator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPassword'
        'Validator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/tutorial/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'tutorial/static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'tutorial/static'),
)
DATE_FORMAT = ('%d/%m/%Y')
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%Y-%m-%d')

# After manage.py check --deploy

CSRF_COOKIE_HTTPONLY = True

# X_FRAME_OPTIONS = 'DENY'
#SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True
