import mimetypes
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL = 'login.Usuario'

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "django_extensions",
    'login',
    'contratacion',
    'certificado',
    'cuentas_cobro'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CONFIGURACIÓN DE ARCHIVOS MEDIA (DOCUMENTOS)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# CORRECCIÓN PARA QUE DJANGO SIRVA ARCHIVOS MEDIA
mimetypes.add_type("text/css", ".css", True)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ⏳ Expirar sesión después de 10 minutos (600 segundos)
SESSION_COOKIE_AGE = 600

# ✅ La sesión expira al cerrar el navegador
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# 🔥 Habilitar sesiones inactivas automáticas
SESSION_SAVE_EVERY_REQUEST = True

LOGIN_URL = '/'
