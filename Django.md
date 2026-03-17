# 🐍 Django Boilerplate

> Guía paso a paso para crear un proyecto Django con buenas prácticas, estructura modular y herramientas esenciales para desarrollo de APIs REST.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#-requisitos-previos)
- [Creación del Proyecto](#-creación-del-proyecto)
- [Dependencias Esenciales](#-dependencias-esenciales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Configuración Inicial](#-configuración-inicial)
- [Apps y Modelos](#-apps-y-modelos)
- [Django REST Framework](#-django-rest-framework)
- [Autenticación](#-autenticación)
- [CORS](#-cors)
- [Variables de Entorno](#-variables-de-entorno)
- [Base de Datos](#-base-de-datos)
- [Herramientas Adicionales](#-herramientas-adicionales)
- [Scripts Útiles](#-scripts-útiles)

---

## 🔧 Requisitos Previos

| Herramienta | Versión Mínima | Instalación |
|-------------|---------------|-------------|
| Python      | 3.11+         | [python.org](https://python.org) |
| pip         | 23.x          | Incluido con Python |
| PostgreSQL  | 15.x          | [postgresql.org](https://postgresql.org) (opcional, SQLite por defecto) |

Verificar instalación:

```bash
python3 --version
pip3 --version
```

---

## 🚀 Creación del Proyecto

```bash
# Crear directorio del proyecto
mkdir <nombre-del-proyecto> && cd <nombre-del-proyecto>

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Instalar Django
pip install django

# Crear proyecto Django
django-admin startproject config .
```

> **¿Por qué `config .`?** Usar `config` como nombre del proyecto mantiene la configuración separada de las apps. El `.` evita crear un directorio extra anidado.

---

## 📦 Dependencias Esenciales

### Instalación en bloque

```bash
pip install \
  djangorestframework \
  django-cors-headers \
  django-environ \
  django-filter \
  drf-spectacular \
  psycopg2-binary \
  gunicorn \
  sentry-sdk
```

### Guardar dependencias

```bash
pip freeze > requirements.txt
```

### Archivo `requirements.txt` recomendado

```txt
django>=5.1,<5.2
djangorestframework>=3.15,<4.0
django-cors-headers>=4.4,<5.0
django-environ>=0.11,<1.0
django-filter>=24.3,<25.0
drf-spectacular>=0.27,<1.0
psycopg2-binary>=2.9,<3.0
gunicorn>=22.0,<23.0
sentry-sdk[django]>=2.0,<3.0
```

Para instalar desde el archivo:

```bash
pip install -r requirements.txt
```

---

## 🏗️ Estructura del Proyecto

```
<nombre-del-proyecto>/
├── config/                            # Configuración del proyecto
│   ├── __init__.py
│   ├── settings/                      # Settings separados por entorno
│   │   ├── __init__.py
│   │   ├── base.py                    # Configuración compartida
│   │   ├── development.py             # Configuración de desarrollo
│   │   └── production.py              # Configuración de producción
│   ├── urls.py                        # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                              # Aplicaciones del proyecto
│   ├── __init__.py
│   ├── users/                         # App de usuarios
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   └── test_views.py
│   │   └── migrations/
│   │       └── __init__.py
│   │
│   └── core/                          # App core (utilidades compartidas)
│       ├── __init__.py
│       ├── models.py                  # Modelos base (TimeStampedModel, etc.)
│       ├── permissions.py             # Permisos personalizados
│       ├── pagination.py              # Paginación personalizada
│       └── exceptions.py              # Excepciones personalizadas
│
├── static/                            # Archivos estáticos
├── media/                             # Archivos subidos por usuarios
├── templates/                         # Templates HTML (si aplica)
│
├── .env                               # Variables de entorno (NO commitear)
├── .env.example                       # Ejemplo de variables de entorno
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Configuración Inicial

### Separar Settings por Entorno

Crea la estructura `config/settings/`:

```bash
mkdir config/settings
touch config/settings/__init__.py
touch config/settings/base.py
touch config/settings/development.py
touch config/settings/production.py
```

### `config/settings/base.py`

```python
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Apps
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
]

LOCAL_APPS = [
    "apps.core",
    "apps.users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "es"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF Spectacular (OpenAPI / Swagger)
SPECTACULAR_SETTINGS = {
    "TITLE": "API",
    "DESCRIPTION": "API Documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
```

### `config/settings/development.py`

```python
from .base import *  # noqa: F401, F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOW_ALL_ORIGINS = True
```

### `config/settings/production.py`

```python
from .base import *  # noqa: F401, F403
import sentry_sdk

DEBUG = False
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DATABASES = {
    "default": env.db("DATABASE_URL"),
}

# CORS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)

# Sentry
sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=""),
    traces_sample_rate=0.1,
)
```

### `config/settings/__init__.py`

```python
import os

environment = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.development")
```

---

## 🧩 Apps y Modelos

### Crear Apps

```bash
mkdir -p apps/core apps/users

# Crear apps dentro del directorio apps/
python manage.py startapp core apps/core
python manage.py startapp users apps/users
```

> Recuerda actualizar el `name` en `apps.py` de cada app:

```python
# apps/users/apps.py
class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"  # ← importante
```

### Modelo Base con Timestamps (`apps/core/models.py`)

```python
from django.db import models


class TimeStampedModel(models.Model):
    """Modelo base abstracto con campos de auditoría."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

### Paginación Personalizada (`apps/core/pagination.py`)

```python
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
```

### Modelo de Usuario Personalizado (`apps/users/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from apps.core.models import TimeStampedModel


class User(AbstractUser):
    """Modelo de usuario personalizado."""

    class Meta:
        db_table = "users"
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return self.email or self.username
```

> Agrega en `config/settings/base.py`:

```python
AUTH_USER_MODEL = "users.User"
```

---

## 🔗 Django REST Framework

### Serializer (`apps/users/serializers.py`)

```python
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id"]
```

### ViewSet (`apps/users/views.py`)

```python
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### URLs de la App (`apps/users/urls.py`)

```python
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls
```

### URLs Principales (`config/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # API
    path("api/v1/", include("apps.users.urls")),

    # API Documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
```

---

## 🔐 Autenticación

### JWT con SimpleJWT (opcional)

```bash
pip install djangorestframework-simplejwt
```

En `config/settings/base.py`:

```python
from datetime import timedelta

REST_FRAMEWORK = {
    # ... configuración existente ...
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
}
```

En `config/urls.py`:

```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns += [
    path("api/v1/auth/token/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

---

## 🌐 CORS

La configuración de CORS ya está incluida con `django-cors-headers`. Asegúrate de que:

1. `"corsheaders"` está en `INSTALLED_APPS`
2. `"corsheaders.middleware.CorsMiddleware"` está en `MIDDLEWARE` (antes de `CommonMiddleware`)
3. Configura los orígenes permitidos:

```python
# Desarrollo (permisivo)
CORS_ALLOW_ALL_ORIGINS = True

# Producción (restrictivo)
CORS_ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
]
```

---

## 🔒 Variables de Entorno

### `.env.example`

```env
# Django
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=config.settings.development

# Database (producción)
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# CORS (producción)
CORS_ALLOWED_ORIGINS=https://tu-dominio.com

# Sentry (producción)
SENTRY_DSN=
```

> **Importante:** Copia `.env.example` a `.env` y ajusta los valores. Nunca commitees `.env`.

```bash
cp .env.example .env
```

### `.gitignore` recomendado

```gitignore
# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/

# Django
db.sqlite3
staticfiles/
media/

# Environment
.env

# IDE
.vscode/
.idea/
```

---

## 🗄️ Base de Datos

### SQLite (Desarrollo — por defecto)

No necesita configuración adicional.

### PostgreSQL (Producción)

```bash
# macOS
brew install postgresql@15

# Crear base de datos
createdb nombre_db
```

En `.env`:

```env
DATABASE_URL=postgres://usuario:contraseña@localhost:5432/nombre_db
```

### Migraciones

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

---

## 🛠️ Herramientas Adicionales

### Ruff (Linter + Formatter)

```bash
pip install ruff
```

Crea `ruff.toml`:

```toml
line-length = 100
target-version = "py311"

[lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[format]
quote-style = "double"
```

### Pre-commit

```bash
pip install pre-commit
```

Crea `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
pre-commit install
```

### pytest (Testing)

```bash
pip install pytest pytest-django
```

Crea `pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.development
python_files = tests.py test_*.py *_tests.py
```

---

## 📜 Scripts Útiles

### Makefile

```makefile
.PHONY: run migrate makemigrations test lint format shell

run:
	python manage.py runserver

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

freeze:
	pip freeze > requirements.txt

setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	cp -n .env.example .env || true
	python manage.py migrate
	@echo "✅ Setup complete!"
```

Uso:

```bash
make run           # Iniciar servidor
make migrate       # Aplicar migraciones
make test          # Ejecutar tests
make lint          # Verificar código
make format        # Formatear código
make setup         # Setup inicial completo
```

---

## ✅ Checklist de Setup

- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`requirements.txt`)
- [ ] Settings separados por entorno
- [ ] Variables de entorno configuradas (`.env`)
- [ ] Modelo de usuario personalizado (`AUTH_USER_MODEL`)
- [ ] Django REST Framework configurado
- [ ] CORS configurado
- [ ] URLs y ViewSets creados
- [ ] Documentación API (Swagger/Redoc) funcionando
- [ ] Migraciones aplicadas
- [ ] Superusuario creado
- [ ] Ruff + pre-commit configurados
- [ ] Tests básicos pasando
- [ ] `.gitignore` configurado

---

> **Hane Boilerplates** — Django Setup Guide
