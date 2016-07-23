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
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null', )
    CAPTCHA_LETTER_ROTATION = None
    DB_ENGINE = 'django.db.backends.sqlite3'
    DB_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
else:
    if socket.gethostname() == 'ubuntu':
        ALLOWED_HOSTS = ['.bugtrack.com']
        DEFAULT_FROM_EMAIL = "info@bugtrack.com"
        DB_ENGINE = 'django.db.backends.sqlite3'
        DB_NAME = os.path.join(BASE_DIR, 'db.sqlite3')
    else:
        # Security
        CSRF_COOKIE_NAME = "cookieXSRF"
        CSRF_COOKIE_SECURE = True
        CSRF_COOKIE_HTTPONLY = True
        SECURE_BROWSER_XSS_FILTER = True
        SECURE_CONTENT_TYPE_NOSNIFF = True

        ALLOWED_HOSTS = ["bugtrack.online", "www.bugtrack.online"]
        DEFAULT_FROM_EMAIL = "info@bugtrack.online"

        DB_ENGINE = 'django.db.backends.mysql'
        DB_NAME = 'bugtrack'
        DB_USER = 'bugtrackuser'
        DB_PASSWORD = r"?5PJ6Q'bGv,@X&yV_f3j"

    ADMINS = (('Ahmed', 'ahmedelantry@gmail.com'), )
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
    STATIC_URL = '/assets/'


# Application definition

INSTALLED_APPS = (
    'passwords',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'ckeditor',
    'django_bleach',
    'app',
    'captcha',
    'registration',
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
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
    }
}
if not DB_ENGINE.endswith('sqlite3'):
    DATABASES['default'].update({
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '3306'
    })

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

# CKEDITOR_UPLOAD_PATH = "uploads/"

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
# Which HTML tags are allowed
BLEACH_ALLOWED_TAGS = [
    'p', 'b', 'i', 'u', 'em', 'strong', 'a',
    'pre', 'code', 'ol', 'ul', 'li', 'hr']

# Which HTML attributes are allowed
BLEACH_ALLOWED_ATTRIBUTES = ['href', 'title', 'style']

# Which CSS properties are allowed in 'style' attributes (assuming
# style is an allowed attribute)
BLEACH_ALLOWED_STYLES = [
    'font-family', 'font-weight', 'text-decoration', 'font-variant']

# Strip unknown tags if True, replace with HTML escaped characters if
# False
BLEACH_STRIP_TAGS = True

# Strip comments, or leave them in.
BLEACH_STRIP_COMMENTS = False

BLEACH_DEFAULT_WIDGET = 'wysiwyg.widgets.WysiwygWidget'

# To send debug messages
SERVER_EMAIL = "debug@bugtrack.online"

# Registration section
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_ACTIVATION_DAYS = 7
PASSWORD_MIN_LENGTH = 8

EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'info@bugtrack.online'
EMAIL_HOST_PASSWORD = r'4`sGRXW]c=J\3;Gfs!{a'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = 'ahmedelantry@gmail.com'
# EMAIL_HOST_PASSWORD = 'xxx'

# SEND_ACTIVATION_EMAIL = False

CAPTCHA_OUTPUT_FORMAT = u'%(hidden_field)s%(image)s %(text_field)s'

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'django-dual-authentication.backends.DualAuthentication'
    ]

SITE_ID = 1
