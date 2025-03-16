"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'product', 'static'),
]
# Медиафайлы (загружаемые пользователями)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6-(&d1@dsp9o&n*_o514e5-#$k)=b5tuoq-87(z^))ekccvsl_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# ALLOWED_HOSTS = []
ALLOWED_HOSTS = [
       'python-shop.onrender.com',
       'localhost',  # если вы тестируете локально
       '127.0.0.1',  # если вы тестируете локально
       # добавьте другие хосты, если необходимо
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'product.apps.SkillsConfig',
    'Purchased.apps.PurchasedConfig',
    'reviews.apps.BlogConfig',
    'rest_framework',
    'rest_framework_simplejwt',
    'social_django',
    'django_extensions',
    'account',
    'allauth',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_celery_results',
    'channels',
    'channel',
]

ASGI_APPLICATION = 'project.asgi.application'
# WSGI_APPLICATION = 'project.wsgi.application'
# redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

# Настройки для Celery
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_WORKER_CONCURRENCY = 1
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sasashiraev543@gmail.com'
EMAIL_HOST_PASSWORD = 'amvpnivjyyocxihx'
DEFAULT_FROM_EMAIL = 'sasashiraev543@gmail.com'
#amvp nivj yyoc xihx

# Юкасса

YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'account.authentication.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',

)
SITE_ID = 1
# Укажите ваши ключи Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '99309848157-17tamkp0pj8esgs8dlkr8icghj41pc4u.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Добавьте URL для обработки возвратов
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
# }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'reviews': {  # Замените на имя вашего проекта
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CSRF_TRUSTED_ORIGINS = [
    'https://python-shop.onrender.com',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
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




# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'pythonshop', # Имя базы данных
#         'USER': 'admin', # Имя пользователя
#         'PASSWORD': 'Global228', # Пароль
#         'HOST': 'host.docker.internal',
#         'PORT': '5432', # Порт (обычно 5432 для PostgreSQL)
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_URL_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DATABASE_URL_NAME', 'pythonshop'),
        'USER': os.environ.get('DATABASE_URL_USER', 'admin'),
        'PASSWORD': os.environ.get('DATABASE_URL_PASSWORD', 'DxJ5Ahiwllt8bmCUUYwDxSxtuWPVqyWU'),
        'HOST': os.environ.get('DATABASE_URL_HOST', 'dpg-cvb7oonnoe9s73fi9klg-a'),
        'PORT': os.environ.get('DATABASE_URL_PORT', '5432'),
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
    # добавьте другие языки по необходимости
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# Статические файлы (CSS, JavaScript, изображения)
# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'product', 'static'),
# ]
# # Медиафайлы (загружаемые пользователями)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
