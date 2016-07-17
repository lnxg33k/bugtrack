"""
Django settings for bugtrack project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pz0l_jwnh5wu_+1u0k92tmf4g+@*@s+9e&e=5!jgkddi6#lk42'

# SECURITY WARNING: don't run with debug turned on in production!

if socket.gethostname() == 'ruined-sec.local':
    DEBUG = True
else:
    DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["*"]
    STATIC_URL = '/static/'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null', )
    CAPTCHA_LETTER_ROTATION = None
else:
    if socket.gethostname() == 'ubuntu':
        ALLOWED_HOSTS = ['.bugtrack.com']
    else:
        ALLOWED_HOSTS = ["bugtrack.online", "www.bugtrack.online"]
    ADMINS = (('Ahmed', 'ahmedelantry@gmail.com'), )
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
    STATIC_URL = '/assets/'


# Application definition

INSTALLED_APPS = (
    'registration',
    'grappelli',
    'passwords',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'app',
    'captcha',
    'preventconcurrentlogins',
    'django-dual-authentication',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'preventconcurrentlogins.middleware.PreventConcurrentLoginsMiddleware',
)

ROOT_URLCONF = 'bugtrack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bugtrack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Qatar'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'), )
# STATIC_URL = '/assets/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
# if not DEBUG:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')

MEDIA_URL = '/media/'

GRAPPELLI_ADMIN_TITLE = "bugTrack"

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                'JustifyBlock', '-', 'HorizontalRule'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source', 'CodeSnippet'],
            ['Maximize', 'ShowBlocks']
        ],
        'width': 760,
        'height': 200,
        'extraPlugins': 'codesnippet',
        'disableNativeSpellChecker': False,
        # 'autoParagraph': False,
    },
}

# Registration section
ACCOUNT_ACTIVATION_DAYS = 7
PASSWORD_MIN_LENGTH = 8
# SEND_ACTIVATION_EMAIL = False

CAPTCHA_OUTPUT_FORMAT = u'%(hidden_field)s%(image)s %(text_field)s'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django-dual-authentication.backends.DualAuthentication'
    ]
