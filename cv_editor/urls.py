from django.urls import path
from . import views

app_name = 'cv_editor'

urlpatterns = [
    path('', views.index, name='index'),
    path('proyectos/', views.project_list, name='project-list'),
]
