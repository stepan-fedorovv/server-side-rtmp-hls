import os
import typing
from pathlib import Path

import structlog
from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    SECRET_KEY = values.Value(default='dev-key')

    DEBUG = values.BooleanValue(default=True)
    ALLOWED_HOSTS = ['*']
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'silk',
        'restdoctor',
        'django_filters',
        'django_structlog',
        'django_celery_results',
        'django_celery_beat',
        'corsheaders',
        'drf_yasg',
        'pgbulk',
        'apps.widget_settings',
        'apps.user',

    ]
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'restdoctor.django.middleware.api_selector.ApiSelectorMiddleware',
        'silk.middleware.SilkyMiddleware',
        # 'django_structlog.middlewares.RequestMiddleware',
    ]

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'apps\\user\\static')

    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

    ROOT_URLCONF = 'config.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
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

    WSGI_APPLICATION = 'config.wsgi.application'

    REST_FRAMEWORK = {
        'DATETIME_FORMAT': '%s',  # for using date and time in timestamp
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'EXCEPTION_HANDLER': 'restdoctor.rest_framework.exception_handlers.exception_handler',
    }

    DATABASES = {
        'default': {
            'ENGINE': values.Value(
                environ_name='DEFAULT_DATABASE_ENGINE', default='django.db.backends.postgresql'
            ),
            'NAME': values.Value(environ_name='DEFAULT_DATABASE_NAME', default='diploma'),
            'USER': values.Value(environ_name='DEFAULT_DATABASE_USER', default='diploma'),
            'PASSWORD': values.Value(environ_name='DEFAULT_DATABASE_PASSWORD', default='diploma'),
            'HOST': values.Value(environ_name='DEFAULT_DATABASE_HOST', default='localhost'),
            'PORT': values.Value(environ_name='DEFAULT_DATABASE_PORT', default='5435'),
        }
    }

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

    LANGUAGE_CODE = 'ru'

    TIME_ZONE = 'UTC'

    USE_I18N = True
    USE_TZ = True
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_HEADERS = (  # noqa: static object
        'x-requested-with',
        'content-type',
        'accept',
        'origin',
        'authorization',
        'x-csrftoken',
        'token',
        'x-device-id',
        'x-device-type',
        'x-push-id',
        'dataserviceversion',
        'maxdataserviceversion',
        'content-disposition',
    )
    # CSRF_TRUSTED_ORIGINS = ['http://localhost:8080/']
    CORS_ALLOW_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS')
    CORS_ORIGIN_WHITELIST = values.ListValue(
        [
            'http://127.0.0.1:3000',
            'http://0.0.0.0:3000',
            'http://localhost:3000',
            'http://localhost:8080',
            'http://127.0.0.1:8080',
            'http://0.0.0.0:8080',
            'https://realdomain',
        ]
    )

    REDIS_HOST = values.Value('localhost')
    REDIS_PORT = values.Value('6379')
    STREAM_KEY = values.Value('some_stream_key')

    # CELERY_LOGGING = {
    #     'version': 1,  # noqa: allowed straight assignment
    #     'disable_existing_loggers': False,  # noqa: allowed straight assignment
    #     'formatters': {
    #         'json_formatter': {
    #             '()': structlog.stdlib.ProcessorFormatter,
    #             'processor': structlog.processors.JSONRenderer(ensure_ascii=False),
    #         },
    #         'plain_console': {
    #             '()': structlog.stdlib.ProcessorFormatter,
    #             'processor': structlog.dev.ConsoleRenderer(),
    #         },
    #     },
    #     'handlers': {  # noqa: static object
    #         'console': {'class': 'logging.StreamHandler', 'formatter': 'plain_console'},
    #         'json_console': {'class': 'logging.StreamHandler', 'formatter': 'json_formatter'},
    #     },
    #     'loggers': {'': {'handlers': ['console'], 'level': 'INFO'}},  # noqa: static object
    # }
    #
    # LOGGING = {
    #     'version': 1,
    #     'disable_existing_loggers': False,
    #     'formatters': {
    #         'json_formatter': {
    #             '()': structlog.stdlib.ProcessorFormatter,
    #             'processor': structlog.processors.JSONRenderer(),
    #         },
    #         'plain_console': {
    #             '()': structlog.stdlib.ProcessorFormatter,
    #             'processor': structlog.dev.ConsoleRenderer(),
    #         },
    #         'key_value': {
    #             '()': structlog.stdlib.ProcessorFormatter,
    #             'processor': structlog.processors.KeyValueRenderer(
    #                 key_order=['timestamp', 'level', 'event', 'logger']
    #             ),
    #         },
    #     },
    #     'handlers': {  # noqa: static object
    #         'console': {
    #             'class': 'logging.StreamHandler',
    #             'formatter': 'plain_console',
    #         },
    #         'json_file': {
    #             'class': 'logging.handlers.WatchedFileHandler',
    #             'filename': 'logs/json.log',
    #             'formatter': 'json_formatter',
    #         },
    #         'flat_line_file': {
    #             'class': 'logging.handlers.WatchedFileHandler',
    #             'filename': 'logs/flat_line.log',
    #             'formatter': 'key_value',
    #         },
    #     },
    #     'loggers': {
    #         'django_structlog': {
    #             'handlers': ['console', 'flat_line_file', 'json_file'],  # noqa: static object
    #             'level': 'INFO',
    #         },
    #         # Make sure to replace the following logger's name for yours
    #         'django_structlog_demo_project': {
    #             'handlers': ['console', 'flat_line_file', 'json_file'],
    #             'level': 'INFO',
    #         },
    #     },
    # }

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    @property
    def CACHES(self) -> dict:
        return {
            'default': {  # noqa: static object
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'legacy-local-cache',
            },
            'redis': {
                'BACKEND': 'django_redis.cache.RedisCache',  # noqa: allowed straight assignment
                'LOCATION': values.Value(
                    'redis://localhost:6379/1', environ_name='REDIS_CACHE_URL'
                ),
                'OPTIONS': {  # noqa: static object
                    'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                    'CONNECTION_POOL_KWARGS': {'max_connections': 20, 'health_check_interval': 30},
                },
            },
        }

    AUTH_USER_MODEL = 'user.User'
    API_DEFAULT_OPENAPI_VERSION = values.Value('3.0.2')
    API_V1_URLCONF = values.Value('configuration.urls')
    API_VENDOR_STRING = values.Value('insurance_backend')
    API_FALLBACK_VERSION = values.Value('fallback')
    API_DEFAULT_VERSION = values.Value('v1')
    API_DEFAULT_FORMAT = values.Value('full')
    API_PREFIXES = values.TupleValue(
        (
            '/api'
        )
    )
    API_FORMATS = values.TupleValue(('full', 'compact'))
    API_RESOURCE_DISCRIMINATIVE_PARAM = values.Value('view_type')
    API_RESOURCE_DEFAULT = values.Value('common')
    API_RESOURCE_SET_PARAM = values.BooleanValue(False)
    API_RESOURCE_SET_PARAM_FOR_DEFAULT = values.BooleanValue(False)

    API_FALLBACK_URLCONF = values.Value('configuration.urls')

    CELERY_BROKER_URL = values.Value('redis://localhost:6379/')
    CELERY_BROKER_TRANSPORT_OPTIONS = values.DictValue({})
    CELERY_ACCEPT_CONTENT = values.ListValue(['application/x-python-serialize'])
    CELERY_TASK_SERIALIZER = values.Value('pickle')
    CELERY_RESULT_SERIALIZER = values.Value('pickle')
    CELERY_CONTENT_ENCODING = values.Value('utf-8')
    CELERY_MAX_TASKS_PER_CHILD = values.IntegerValue(100)
    CELERY_BROKER_HEARTBEAT = values.IntegerValue(0)
    CELERY_RESULT_BACKEND = values.Value('django-db')
    CELERY_TASK_DEFAULT_QUEUE = values.Value('insurance_backend-default')
    CELERY_RESULT_EXPIRES = values.Value(None)
    CELERY_TASK_ALWAYS_EAGER = values.BooleanValue(False)
    CELERY_CACHE_BACKEND = values.Value('default')
