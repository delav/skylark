"""
Django settings for skylark project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from pathlib import Path
from loguru import logger
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# log setting
server_log_file_path = os.path.join(BASE_DIR, "logs/server.log")
error_log_file_path = os.path.join(BASE_DIR, "logs/error.log")
logger.add(server_log_file_path, rotation="50 MB", encoding="utf-8", level="INFO")
logger.add(error_log_file_path, rotation="50 MB", encoding="utf-8", level="ERROR")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h--jee4sh9uvpfsd5(3shn44e&fhcog9@lro82%2@7dcq_eaqy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'application.user.apps.UserConfig',
    'application.group.apps.GroupConfig',
    'application.casetag.apps.CaseTagConfig',
    'application.keywordgroup.apps.KeywordGroupConfig',
    'application.libkeyword.apps.LibKeywordConfig',
    'application.project.apps.ProjectConfig',
    'application.suitedir.apps.SuiteDirConfig',
    'application.testsuite.apps.TestSuiteConfig',
    'application.testcase.apps.TestCaseConfig',
    'application.caseentity.apps.CaseEntityConfig',
    'application.userkeyword.apps.UserKeywordConfig',
    'application.setupteardown.apps.SetupTeardownConfig',
    'application.variable.apps.VariableConfig',
    'application.builder.apps.BuilderConfig',
    'application.buildcase.apps.BuildCaseConfig',
    'application.environment.apps.EnvironmentConfig',
    'application.casepriority.apps.CasePriorityConfig',
    'application.pythonlib.apps.PythonlibConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'skylark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': []
        ,
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

WSGI_APPLICATION = 'skylark.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 3600,
        'NAME': 'skylark',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '729814'
    }
}

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'application.infra.permission.LoginAuth',
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'EXCEPTION_HANDLER': 'application.infra.exception.exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
}

CORS_ORIGIN_ALLOW_ALL = True

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AES_KEY = "20220427@)@@)$@&"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = os.path.join(BASE_DIR, 'static/media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# model data type. 0: test case, 1: resource(user keyword), 2: text/other file
MODEL_TYPE = (
    (0, 'TestCase'),
    (1, 'Resource'),
    (2, 'HelpFile'),
)

# Python keyword directory
LIB_URL = '/library/'

# Default copy project
PROJECT_MODULE = 'SKYLARK'

# Tree default node data
NODE = {'id': 1, 'pId': 0, 'name': 'DEFAULT', 'desc': None, 'type': 0, 'open': True, 'nocheck': False}

