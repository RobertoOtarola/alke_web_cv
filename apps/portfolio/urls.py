from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('proyectos/', views.project_list, name='project-list'),
    path('caso-de-estudio/<slug:slug>/', views.case_study_detail, name='case-study'),
]
