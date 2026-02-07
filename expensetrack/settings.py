"""
Django settings for expensetrack project.
Local demo configuration – fully working
"""

from pathlib import Path
import os
from django.contrib import messages

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# ENVIRONMENT (SAFE DEFAULT)
# ===============================
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

# ===============================
# SECURITY
# ===============================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-demo-key-123456'
)

DEBUG = True

ALLOWED_HOSTS = ['ganesh.pythonanywhere.com']

# ===============================
# APPLICATIONS
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'core',
    'authentication',
    'preferences',
    'incomes',

    # Tailwind & reload
    'tailwind',
    'theme',
    'django_browser_reload',
]

TAILWIND_APP_NAME = 'theme'

# Windows npm path
NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

INTERNAL_IPS = [
    "127.0.0.1",
]

# ===============================
# MIDDLEWARE
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# ===============================
# URLS / TEMPLATES
# ===============================
ROOT_URLCONF = 'expensetrack.urls'

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

WSGI_APPLICATION = 'expensetrack.wsgi.application'

# ===============================
# DATABASE (SQLITE – NO SETUP)
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ===============================
# PASSWORD VALIDATION
# ===============================
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

# ===============================
# INTERNATIONALIZATION
# ===============================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# ===============================
# STATIC FILES
# ===============================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ===============================
# DEFAULT PRIMARY KEY
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===============================
# MESSAGE TAGS
# ===============================
MESSAGE_TAGS = {
    messages.ERROR: 'red',
    messages.SUCCESS: 'green',
}
