from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "portfolio"

urlpatterns = [
    # Vista principal (Grid de proyectos destacados)
    path("", views.portfolio_index, name="index"),

    # Caso de estudio específico
    path("caso-estudio/<slug:slug>/", views.case_study_detail, name="case-study"),

    # Redirección de la ruta antigua (301)
    path("proyectos/", RedirectView.as_view(pattern_name="portfolio:index", permanent=True), name="proyectos_redirect"),
]
