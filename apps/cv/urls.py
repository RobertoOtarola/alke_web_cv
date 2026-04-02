from django.urls import path
from . import views

app_name = "cv"

urlpatterns = [
    path("", views.index, name="index"),
    path("proyectos/", views.project_list, name="project-list"),
]
