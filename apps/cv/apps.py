from django.apps import AppConfig


class CvConfig(AppConfig):
    name = "apps.cv"
    default_auto_field = "django.db.models.BigAutoField"  # CR-29: explícito por buena práctica
