"""
Django settings for lti_tool project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l+ft&uk)ly#$^-#v&0#b^g#laa-v-k*(aedi#$#b2(k@fl_w4!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['lti-unifecaf-sample.app.unifecaf.edu.br','localhost','fecaf.brightspace.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'csp',
    'lti_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Must be included
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Use secure cookies in production
SESSION_COOKIE_SECURE = True  # Set to True in production with HTTPS

# Allow cookies to be sent in cross-site requests
SESSION_COOKIE_SAMESITE = 'None' 

# Ensure the session engine is using the database
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_COOKIE_SECURE = True  # Set to True in production with HTTPS
CSRF_COOKIE_SAMESITE = 'None' 
SECURE_SSL_REDIRECT = False  # Do not redirect HTTP to HTTPS

ROOT_URLCONF = 'lti_tool.urls'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[{asctime}] {levelname} {name} {message}",
            'style': '{',
        },
        'simple': {
            'format': "{levelname} {message}",
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'lti_app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Include if you have project-level templates
        'APP_DIRS': True,  # This allows Django to look for templates inside each app's 'templates' directory
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

WSGI_APPLICATION = 'lti_tool.wsgi.application'

CSRF_TRUSTED_ORIGINS = ['https://fecaf.brightspace.com']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Absolute path to the database file
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

USE_X_FORWARDED_HOST = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSP_FRAME_ANCESTORS = (
    'https://fecaf.brightspace.com',  # Replace with your LMS domain
    'https://*.brightspace.com',       # If Brightspace uses subdomains    
)

CSP_SCRIPT_SRC = (
    "'self'",
    'https://fecaf.brightspace.com',  # Add any additional trusted sources
    "'unsafe-inline'",  # Not recommended
)

CSP_STYLE_SRC = (
    "'self'",
    "https://lookerstudio.google.com",
    "'unsafe-inline'",  # Not recommended
)

CSP_FRAME_SRC = (
    "'self'",  # Allow iframe to load from the same origin
    'https://lookerstudio.google.com',
)
