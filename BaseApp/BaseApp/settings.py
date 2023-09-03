import logging
import mimetypes
import os
from pathlib import Path

mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
mimetypes.add_type("text/javascript", ".min.js", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-2a#v8eo^=11y_ym6zlzctlvh7_z+*)x+4b)#euf!uf$49_eb#s'

DEBUG = True
print("DEBUG\t", DEBUG)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    # "sslserver",
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'ecommerce',
    'rest_framework',
    # 'system',
    'elearning',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BaseApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


print("TEMPLATE DIR ", os.path.join(BASE_DIR, 'templates'))

WSGI_APPLICATION = 'BaseApp.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'baseapp4',
        'USER': 'root',
        'PASSWORD': 'rootroot',
        'HOST': 'localhost',
        'PORT': '',
    }
}
'''
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True

print("TIME ZONE ", TIME_ZONE)

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')
# for nginx
STATIC_ROOT = '/static_files/'

STATICFILES_DIRS = [
    # '/var/www/static/',
    # BASE_DIR / 'static'
    os.path.join(BASE_DIR, 'static')
]

print("STATIC ROOT ", STATIC_ROOT)

# Base url to serve media files
MEDIA_URL = '/media/'
# MEDIA_URL = '/C:\inetpub\wwwroot\BaseApp\media/'

# Path where media is stored
# MEDIA_ROOT = str(os.path.join(BASE_DIR, 'media')).replace('\\', '/')
MEDIA_ROOT = str(os.path.join(BASE_DIR, 'media'))

# nginx
# MEDIA_ROOT = '/media/'
print("MEDIA ROOT ", MEDIA_ROOT)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SSL & session time out auto logout
# CSRF_COOKIE_SECURE=True
# SESSION_COOKIE_SECURE=True
# SESSION_COOKIE_AGE=300

# nginx
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1"]
# DB
# CONN_MAX_AGE=0
LOGGING_CONFIG = None

# logging.config.dictConfig(...)
logging.basicConfig(
    filemode='w',
    level=logging.INFO,
    filename=os.path.join('dve-application.log'),
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

print("\n\n***************************************************")
