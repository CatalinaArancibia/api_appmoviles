"""
Django settings for ecoapi project.
Corregido para soporte JWT, MySQL/SQLite híbrido y CORS.
"""

from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Si no hay clave en .env, usa una por defecto para desarrollo
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-clave-temporal-dev-12345")

# SECURITY WARNING: don't run with debug turned on in production!
# Convertimos el string 'True'/'False' del .env a booleano real
DEBUG = os.getenv("DEBUG", "False") == "True"

# Permitir cualquier host (necesario para AWS y pruebas desde móvil)
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- LIBRERÍAS DE TERCEROS ---
    'rest_framework',
    'rest_framework_simplejwt', # JWT para autenticación
    'corsheaders',              # Para permitir conexión desde Android/Web externa
    
    # --- TUS APPS ---
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # <-- OBLIGATORIO AL PRINCIPIO
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecoapi.urls'

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

WSGI_APPLICATION = 'ecoapi.wsgi.application'


# ==============================================================================
# CONFIGURACIÓN DE BASE DE DATOS (INTELIGENTE)
# ==============================================================================
# Si en el .env definimos un DB_HOST, intentamos usar MySQL.
# Si no (como en local), usamos SQLite.
DB_HOST = os.getenv('DB_HOST')

if DB_HOST:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': DB_HOST,
            'PORT': os.getenv('DB_PORT', '3306'),
        }
    }
else:
    # Configuración para Desarrollo Local (SQLite)
    print("⚠️  AVISO: Usando SQLite local (No se encontraron datos MySQL en .env)")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==============================================================================
# CONFIGURACIÓN DE AUTENTICACIÓN Y JWT
# ==============================================================================

# Indicamos que usamos TU modelo de usuario personalizado
AUTH_USER_MODEL = 'api.Usuario'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny', # Por defecto abierto, cerramos en views
    ],
}

# Configuración del Token JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ==============================================================================
# CORS (Permisos para que Android/Arduino se conecten)
# ==============================================================================
CORS_ALLOW_ALL_ORIGINS = True  # Acepta conexiones de cualquier IP


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'es-cl' # Español Chile
TIME_ZONE = 'America/Santiago' # Hora de Chile
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'