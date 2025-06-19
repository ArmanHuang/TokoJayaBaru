import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-aae%yr_wjv$@!*)ves=mvlz!hr@0%(&8!i%^fvw716w+1cch8j'
DEBUG = True
ALLOWED_HOSTS = ['31.97.51.94', 'tokojayabaru.com', 'www.tokojayabaru.com']

INSTALLED_APPS = [
    'jazzmin',
    'landingpage',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise di middleware sebelum CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TokoJayaBaru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Bisa ditambahkan folder template custom jika ada
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TokoJayaBaru.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Folder sumber static files kamu selama development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Folder hasil 'collectstatic' (untuk production & Nginx/WhiteNoise)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Storage backend WhiteNoise untuk compress & cache busting
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Password validation, JAZZMIN_SETTINGS, dan lain-lain tetap sama ...
