"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.http import HttpResponse

def health_check(request):
    """Básico endpoint de health check."""
    return HttpResponse("ok")

urlpatterns = [
    # Panel de administración (URL Configurada por env variable)
    path(settings.ADMIN_URL, admin.site.urls),

    # CV personal (Página de inicio principal)
    path('', include('apps.cv.urls', namespace='cv')),

    # Portafolio y Casos de Estudio
    path('portfolio/', include('apps.portfolio.urls', namespace='portfolio')),

    # DevOps Health Check
    path('health/', health_check, name='health'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
