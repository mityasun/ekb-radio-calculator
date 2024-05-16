import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='default-value')

DEBUG = os.getenv('DEBUG', default=False)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(' ')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'django_filters',

    'utils.apps.UtilsConfig',
    'settings.apps.SettingsConfig',
    'users.apps.UsersConfig',
    'stations.apps.StationsConfig',
    'rates.apps.RatesConfig',
    'discounts.apps.DiscountsConfig',
    'customers.apps.CustomersConfig',
    'orders.apps.OrdersConfig',
    'api.apps.ApiConfig'
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

ROOT_URLCONF = 'backend.urls'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cache settings

# CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": f"redis://redis:{os.getenv('REDIS_PORT')}/",
#             "OPTIONS": {
#                 "PASSWORD": os.getenv('REDIS_PASSWORD'),
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient"
#             },
#         }
#     }

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 60

# Logging settings

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         }
#     }
# }


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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True

CORS_URLS_REGEX = r'^/api/.*$'

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split(' ')

APPEND_SLASH = True

LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 100,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# Project variables

NAME: int = 100
DESCRIPTION: int = 5000
BROADCAST_ZONE: int = 200
MIN_LENGTH: int = 1
MIN_AUDIO_DURATION: int = 1
MAX_AUDIO_DURATION: int = 100
MIN_RATE: int = 0
MAX_RATE: int = 100
MIN_REACH_DLY: int = 0
MAX_REACH_DLY: int = 10000000
MIN_PERCENT: int = 0
MAX_PERCENT: int = 100
MIN_PRICE: int = 0
MAX_PRICE: int = 10000000
MIN_DAY: int = 1
MAX_DAY: int = 180
MIN_VOLUME_ORDER: int = 1
MAX_VOLUME_ORDER: int = 527
MIN_PHONE: int = 11
PHONE: int = 18
MIN_EMAIL: int = 6
EMAIL: int = 100
MIN_USERNAME: int = 3
USERNAME: int = 50
FIRST_NAME: int = 100
LAST_NAME: int = 100
MIN_PASSWORD: int = 8
PASSWORD: int = 150
MIN_SEARCH: int = 3
MAX_SEARCH: int = 50
BIG_TEXT: int = 20000
IMAGE_SIZE: int = 1280
PHOTO_QUALITY: int = 90
PHOTO_RATIO: int = 4
MIN_IMAGE_RESOLUTION: int = 500
MAX_IMAGE_RESOLUTION: int = 3000
MAX_IMAGE_SIZE: int = 1048576
DEFAULT_LOGO: str = 'default_images/default-station.jpg'
DEFAULT_COMPANY_LOGO: str = 'default_images/default-company.png'
MAX_LIMIT: int = 100
SEO_TITLE: int = 150
SEO_DESCRIPTION: int = 300
SEO_KEYWORDS: int = 200
COPYRIGHT: int = 200
ADDRESS: int = 200


# E-mail settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = False
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
ORDER_TO_EMAIL = os.getenv('ORDER_TO_EMAIL')

