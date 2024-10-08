"""
Django settings for flower_delivery project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from config import SECRET_KEY, TELEGRAM_BOT_TOKEN


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Путь к корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECURITY WARNING: don't run with debug turned on in production!
# Ключ безопасности
SECRET_KEY = SECRET_KEY

# Режим отладки
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = []


# Подключение приложений

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flowers',  # Приложение для товаров
    'orders',   # Приложение для заказов
    'bot',      # Приложение для Telegram бота
    'users',    # Приложение для авторизации/регистрации пользователей
]
# Настройки посредников (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Настройки URL проекта
ROOT_URLCONF = 'flower_delivery.urls'




# Пути к шаблонам
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

# WSGI приложение
WSGI_APPLICATION = 'flower_delivery.wsgi.application'

# Настройки базы данных
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Настройки аутентификации
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/
# Локализация
LANGUAGE_CODE = 'ru-ru'

# Временная зона
TIME_ZONE = 'Europe/Moscow'

# Поддержка международных форматов времени
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
# Настройки статических файлов (CSS, JavaScript, изображения)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Папка для загружаемых файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Настройка бота (Telegram API)
TELEGRAM_BOT_TOKEN = '7424549025:AAHAgHHj4R2arJxk5mZYAlnM5MVA9xsfKkg'

TELEGRAM_CHAT_ID = '7424549025'

# Настройки Django

DJANGO_SERVER_URL = 'http://127.0.0.1:8000'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
# Настройки для загрузки файлов и статиков

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Перенаправление после входа
LOGIN_REDIRECT_URL = '/'


