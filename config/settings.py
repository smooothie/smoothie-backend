import os

import dj_database_url
import dotenv

dotenv.load()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEROKU = dotenv.get('HEROKU', default=False)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dotenv.get('SECRET_KEY', default='fhp%l9_8v^42!$lij&x8maw+5@p6&#e_sy9(6g89%qmtpo+slc')

PRODUCTION = dotenv.get('ENV') == 'production'
TEST = dotenv.get('ENV') == 'test'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not PRODUCTION

ALLOWED_HOSTS = [
    'smoooth.ieee',
    'smooothie.xyz',
    'smooothie-web.herokuapp.com',
    'smooothie-backend.herokuapp.com'
] if PRODUCTION else ['*']


# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'corsheaders',
    'djmoney',
    'graphene_django',
    'polymorphic',

    # local
    'apps.accounts',
    'apps.common',
    'apps.counterparties',
    'apps.transactions',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {'default': None}

if not HEROKU:
    # Change 'default' database configuration with $DATABASE_URL.
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


DEFAULT_CURRENCY = 'UAH'

if not HEROKU:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(asctime)s\t%(levelname)s\t%(name)s, line %(lineno)s\t'
                          '%(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }


GRAPHENE = {
    'SCHEMA': 'apps.schema.schema',
    'SCHEMA_OUTPUT': 'static/schema.json',
    'SCHEMA_INDENT': 2,
    'CAMELCASE_ERRORS': True,
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

API_URL = dotenv.get('API_URL', default='http://localhost:8000')
UI_URL = dotenv.get('UI_URL', default='http://localhost:3000')

if PRODUCTION:
    CORS_ORIGIN_WHITELIST = [UI_URL]
else:
    CORS_ORIGIN_REGEX_WHITELIST = [
        r'^(http://)?(localhost|127\.0\.0\.1)(:\d+)?$',
        r'^(https?://)?(\w+\.)?smooothie-web-test(-pr-\d+)?\.herokuapp\.com$',
        r'^(https?://)?(\w+\.)?smooothie-web(-staging)?\.herokuapp\.com$',
    ]

CORS_URLS_REGEX = r'^/graphql$'

CSRF_TRUSTED_ORIGINS = [UI_URL]

if HEROKU:
    import django_heroku
    django_heroku.settings(locals(), staticfiles=False, allowed_hosts=False, secret_key=False)
