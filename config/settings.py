import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',  #nuestra app
]

TEMPLATES = [
    {
        ...
        'DIRS': [BASE_DIR / 'templates'],  #carpeta global de templates
        ...
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  #carpeta para archivos estáticos

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  #para imágenes subidas