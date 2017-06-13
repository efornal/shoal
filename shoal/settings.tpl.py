# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Django settings for shoal project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import logging
import os
import ldap
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPLICATION_NAME= "Shoal"
APPLICATION_DESC= "LDAP Users"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vp7p0c223vc98k_qx31op8c18s9&x*1kvott8**zbjc+ec3t%!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'jquery_ui',
    'bootstrap_ui',
    'django_extensions',
    'bootstrap_themes',
    'app',
    'ldap_people',
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
    'django.middleware.locale.LocaleMiddleware',
    'app.middleware.ForceLangMiddleware',
]

ROOT_URLCONF = 'shoal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'ldap_people/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shoal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shoal_db',
        'USER': 'shoal_user',
        'PASSWORD': 'user',
        'PORT': '5432',
        'HOST': 'localhost',
    },
    'shoal_owner': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shoal_db',
        'USER': 'shoal_owner',
        'PASSWORD': 'owner',
        'PORT': '5432',
        'HOST': 'localhost',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'es'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

LOCALE_PATHS = (
     BASE_DIR + '/locale', )

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGIN_URL='/app/login/'
LOGIN_REDIRECT_URL = '/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# django configuration
SUIT_CONFIG = {
    'ADMIN_NAME': APPLICATION_NAME
}

# =================================\
# ldap configuration
LDAP_SERVER = 'ldap://ldap_host:389'
-LDAP_DN = 'dc=*,dc=*,dc=*,dc=*'

# Organizational Unit for Person
LDAP_GROUP  = 'Group' # ou=Entry
LDAP_PEOPLE = 'People' # ou=Entry

LDAP_USERNAME='username'
LDAP_PASSWORD='password'
#
# Maximum limit of results to be taken as error
LDAP_SIZE_LIMIT=100
#
# If specified, add the ObjectClass to the search condition of ldap
LDAP_FILTER_OBJECT_CLASS=[]
#
# Domain name used to identify the institutional mail of an alternative
# Ej: the (LDAP DN)
LDAP_DOMAIN_MAIL=''

# Performs filtering to obtain LDAP groups
# min group_id (group_id>= 500) for ldap search filter
LDAP_GROUP_MIN_VALUE = 500 
# Shows additional information in the search if the registered user
# belongs to any of the indicated groups
GROUPS_EXTRA_INFORMATION_SEARCH = []

# =================================/


# =================================\
# django ldap configuration
#
#
# Ldap Group Type
from django_auth_ldap.config import LDAPSearch, PosixGroupType
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou={},{}".format(LDAP_GROUP,LDAP_DN),
                                    ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE =  PosixGroupType()
#
#
# User will be updated with LDAP every time the user logs in.
# Otherwise, the User will only be populated when it is automatically created.
AUTH_LDAP_ALWAYS_UPDATE_USER = True
#
#
# Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN)
# AUTH_LDAP_DENY_GROUP = "cn=denygroup,ou={},{}".format(LDAP_GROUP,LDAP_DN)
#
# Defines the django admin attribute
# according to whether the user is a member or not in the specified group
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN),
    "is_staff": "cn=users,ou={},{}".format(LDAP_GROUP,LDAP_DN),
    "is_superuser": "cn=admin,ou={},{}".format(LDAP_GROUP,LDAP_DN),
}
#
# Ldap User Auth
AUTH_LDAP_BIND_DN = "cn={},{}".format(LDAP_USERNAME,LDAP_DN)
AUTH_LDAP_BIND_PASSWORD = LDAP_PASSWORD

AUTH_LDAP_SERVER_URI = LDAP_SERVER

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou={},{}".format(LDAP_PEOPLE,LDAP_DN),
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
#    'django.contrib.auth.backends.ModelBackend',
)

# =================================/

#loggin querys in develompent
# if DEBUG:
#     l = logging.getLogger('django.db.backends')
#     l.setLevel(logging.DEBUG)
#     l.addHandler(logging.StreamHandler())
#     logging.basicConfig(
#         level = logging.DEBUG,
#         format = " %(levelname)s %(name)s: %(message)s",
#     )


# logger = logging.getLogger('django_auth_ldap')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.DEBUG)
