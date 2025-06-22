import os  # Add this line to import the os module

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-aae%yr_wjv$@!*)ves=mvlz!hr@0%(&8!i%^fvw716w+1cch8j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['tokojayabaru.com', 'www.tokojayabaru.com', '31.97.51.94']



# Application definition

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
        'DIRS': [],
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # This will now work as expected
]

STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

JAZZMIN_SETTINGS = {
    "site_title": "Admin Toko Jaya Baru",
    "site_header": "Toko Jaya Baru Dashboard",
    "site_brand": "Toko Jaya Baru",
    "welcome_sign": "Selamat datang di Admin Toko Jaya Baru",

    "custom_css": "css/admin.css", 
    "site_logo": "assets/logo-2.png", 

    "icons": {
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "landingpage.PredictionResult": "fas fa-chart-line",  
        "landingpage.ProductCategory": "fas fa-th-list",  
        "landingpage.Product": "fas fa-box",
    },

    "show_sidebar": True,
    "navigation_expanded": True,

    # "side_menu": [
    #     {
    #         "app": "landingpage",
    #         "model": "PredictionResult",
    #         "name": "Prediction Results",
    #         "icon": "fas fa-chart-line"
    #     },
    #     {
    #         "app": "landingpage",
    #         "model": "ProductCategory",
    #         "name": "Product Categories",
    #         "icon": "fas fa-th-list"
    #     },
    #     {
    #         "app": "landingpage",
    #         "model": "Product",
    #         "name": "Products",
    #         "icon": "fas fa-box"
    #     }
    # ]
}
