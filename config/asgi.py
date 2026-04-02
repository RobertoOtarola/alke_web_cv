"""
ASGI config para alke_web_cv.

Documentación: https://docs.djangoproject.com/en/stable/howto/deployment/asgi/

El valor por defecto apunta a 'local'. En producción (Render), la variable
de entorno DJANGO_SETTINGS_MODULE sobreescribe este valor automáticamente
con 'config.settings.production'.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

application = get_asgi_application()
