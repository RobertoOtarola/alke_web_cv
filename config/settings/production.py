"""
Configuración de Django para el entorno de producción (Render + Supabase).

Variables de entorno requeridas en Render:
    SECRET_KEY             → clave secreta Django (mínimo 50 caracteres)
    DATABASE_URL           → connection string Supabase (Transaction Pooler, puerto 6543)
    ALLOWED_HOSTS          → dominios separados por coma: tu-app.onrender.com,tudominio.cl
    DJANGO_SETTINGS_MODULE → config.settings.production
    DJANGO_ADMIN_URL       → URL secreta del admin, ej: miadmin-xyz123/ (default: admin-secret/)

Opcionales (Cloudinary para media en Render Free Tier):
    CLOUDINARY_CLOUD_NAME  → cloud name
    CLOUDINARY_API_KEY     → API key
    CLOUDINARY_API_SECRET  → API secret

Opcionales (correo):
    EMAIL_HOST_USER        → cuenta SMTP
    EMAIL_HOST_PASSWORD    → contraseña SMTP
"""

import dj_database_url
from decouple import config

from .base import *  # noqa: F401, F403

# ─── DEBUG ────────────────────────────────────────────────────────────────────
# NUNCA activar en producción.
DEBUG = False

# ─── HOSTS PERMITIDOS ─────────────────────────────────────────────────────────
# Variable de entorno OBLIGATORIA: ALLOWED_HOSTS=tu-app.onrender.com,tudominio.cl
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

# ─── BASE DE DATOS ────────────────────────────────────────────────────────────
# Usar el Transaction Pooler de Supabase (puerto 6543), no la conexión directa.
# ssl_require=True garantiza cifrado en tránsito — obligatorio en Supabase.
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),   # falla explícito si no está definida (CR-03)
        conn_max_age=600,
        ssl_require=True,                 # CR-04: SSL obligatorio para Supabase
    )
}

# ─── ALMACENAMIENTO DE ARCHIVOS (Cloudinary) ──────────────────────────────────
# Necesario para persistencia de medios en Render (Free Tier sin disco persistente).
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY":    config("CLOUDINARY_API_KEY",    default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# ─── CORREO (opcional) ────────────────────────────────────────────────────────
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")

# ─── SEGURIDAD HTTPS ──────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31_536_000          # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# CR-05: SECURE_BROWSER_XSS_FILTER eliminado — deprecado desde Django 4.0.

# ─── LOGGING ──────────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
