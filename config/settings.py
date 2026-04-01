import os
from pathlib import Path

# 1. Rutas Básicas
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Seguridad (Mantener en secreto en producción)
SECRET_KEY = 'django-insecure-tu-clave-secreta-aqui'
DEBUG = True
ALLOWED_HOSTS = []

# 3. Aplicaciones del Proyecto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',  # Tu aplicación principal [cite: 37]
]

# 4. Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# 5. Plantillas y Procesadores de Contexto
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Carpeta global de templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'tienda.context_processors.cart_total_items', # Para el contador del carrito
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 6. Base de Datos (SQLite por defecto para el proyecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. Internacionalización (Ajustado para Argentina)
LANGUAGE_CODE = 'es-ar' # Cambiado a español Argentina
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# 8. Archivos Estáticos y Media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 9. Configuración de Autenticación (CORREGIDO)
# Usamos los 'name' definidos en urls.py
LOGIN_URL = 'login' 
LOGIN_REDIRECT_URL = 'index' 
LOGOUT_REDIRECT_URL = 'login'
