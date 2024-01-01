"""
Django settings for skylark project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import sys
from pathlib import Path
from loguru import logger
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add worker to python path
sys.path.insert(1, str(BASE_DIR / 'worker'))

# Log setting
server_log_file_path = BASE_DIR / 'log/server.log'
error_log_file_path = BASE_DIR / 'log/error.log'
logger.add(server_log_file_path, rotation="100 MB", encoding="utf-8", level="INFO")
logger.add(error_log_file_path, rotation="100 MB", encoding="utf-8", level="ERROR")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h--jee4sh9uvpfsd5(3shn44e&fhcog9@lro82%2@7dcq_eaqy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# AUTH_USER_MODEL = 'application.user.User'

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
    'django_celery_beat',
    'application.systemext.apps.SystemExtConfig',
    'application.user.apps.UserConfig',
    'application.usergroup.apps.UserGroupConfig',
    'application.department.apps.DepartmentConfig',
    'application.projectpermission.apps.ProjectPermissionConfig',
    'application.tag.apps.TagConfig',
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
    'application.virtualfile.apps.VirtualFileConfig',
    'application.builder.apps.BuilderConfig',
    'application.buildplan.apps.BuildPlanConfig',
    'application.buildrecord.apps.BuildRecordConfig',
    'application.buildhistory.apps.BuildHistoryConfig',
    'application.environment.apps.EnvironmentConfig',
    'application.region.apps.RegionConfig',
    'application.casepriority.apps.CasePriorityConfig',
    'application.pythonlib.apps.PythonlibConfig',
    'application.projectversion.apps.ProjectVersionConfig',
    'application.notification.apps.NotificationConfig',
    'application.webhook.apps.WebhookConfig',
    'application.executeparam.apps.ExecuteParamConfig',
    'application.workermanager.apps.WorkerManagerConfig',
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
    'infra.django.middleware.loghandler.OpLogs',
]

ROOT_URLCONF = 'skylark.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'static/templates'],
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
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}

# Redis
REDIS = {
    'HOST': '127.0.0.1',
    'PORT': '6379',
    'PASSWORD': '',
}

# cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS.get("HOST")}:{REDIS.get("PORT")}/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
    }
}

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'infra.django.permission.LoginAuth',

    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'EXCEPTION_HANDLER': 'infra.django.exception.exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
}

# cors setting
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    '*',
)
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
)
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PATCH',
    'OPTIONS',
    'PUT',
    'DELETE',
    'VIEW',
)

# server url
SERVER_DOMAIN = '127.0.0.1:8000'

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

TIME_ZONE = 'Asia/Shanghai'

DJANGO_CELERY_BEAT_TZ_AWARE = False

USE_I18N = True

USE_L10N = True

USE_TZ = False

AES_KEY = '20220427@)@@)$@&'

INTERNAL_KEY = "123!@#"

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'admin@skylark.com'
EMAIL_HOST_PASSWORD = 'xxxxxx'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

SYSTEM_FILES = BASE_DIR / 'files/systemfiles'

PROJECT_FILES = BASE_DIR / 'files/projectfiles'
FILE_SIZE_LIMIT = 10 * 1024 * 1024
SAVE_TO_DB_SIZE_LIMIT = 1 * 1024 * 1024
VARIABLE_FILE_TYPE = ('.py', '.yaml')
SAVE_TO_DB_FILE_TYPE = ()

# distributed execute
DISTRIBUTED_BUILD = True
DISTRIBUTED_BY_SUITE = True
WORKER_MAX_CASE_LIMIT = 200

# keyword icon path
KEYWORD_ICON_PATH = MEDIA_ROOT / 'icons' / 'keyword'

# Customized python lib keyword path
LIBRARY_BASE_DIR = BASE_DIR.parent
LIBRARY_GIT = 'https://github.com/delav/skylarklibrary.git'
LIBRARY_PATH = BASE_DIR.parent / 'skylarklibrary'

# Robot report path
REPORT_PATH = BASE_DIR / 'report'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

# Default copy project
PROJECT_MODULE = 'SKYLARK'

# result redis
REDIS_URL = f'redis://{REDIS.get("HOST")}:{REDIS.get("PORT")}/1'
REDIS_EXPIRE_TIME = 60*60*24*2


# Celery task imports
CELERY_TASKS_IMPORTS = (
    'task.builder.tasks',
    'task.robot.tasks',
    'task.version.tasks',
    'task.reporter.tasks',
    'task.exchange.tasks'
)
# Celery queues
DEFAULT_QUEUE = 'default'
RUNNER_QUEUE = 'runner'
NOTIFIER_QUEUE = 'notifier'
BUILDER_QUEUE = 'builder'
EXCHANGE_QUEUE = 'exchanger'
# Celery tasks
NOTIFIER_TASK = 'task.robot.tasks.robot_notifier'
RUNNER_TASK = 'task.robot.tasks.robot_runner'
INSTANT_TASK = 'task.builder.tasks.instant_builder'
PERIODIC_TASK = 'task.builder.tasks.periodic_builder'
REPORT_TASK = 'task.reporter.tasks.send_report'
VERSION_TASK = 'task.version.tasks.generate_version'
HEARTBEAT_TASK = 'task.exchange.tasks.heartbeat'
COLLECTOR_TASK = 'task.exchange.tasks.worker_collector'
COMMAND_TASK = 'task.exchange.tasks.command_executor'
# Celery periodic tasks
CELERY_PERIOD_TASKS = {
    'clear_expired_file': {
        'task': 'task.period.clear_expired_file',
        'schedule': timedelta(days=7)
    },
}

CELERY_TASK_CONF = [
    {
        'queue': DEFAULT_QUEUE,
        'tasks': [
            VERSION_TASK,
            REPORT_TASK,
        ]
    },
    # {
    #     'queue': RUNNER_QUEUE,
    #     'tasks': []
    # },
    {
        'queue': NOTIFIER_QUEUE,
        'tasks': [
            NOTIFIER_TASK
        ]
    },
    {
        'queue': BUILDER_QUEUE,
        'tasks': [
            INSTANT_TASK,
            PERIODIC_TASK
        ]
    },
    {
        'queue': EXCHANGE_QUEUE,
        'tasks': [
            HEARTBEAT_TASK,
            COLLECTOR_TASK
        ]
    }
]


