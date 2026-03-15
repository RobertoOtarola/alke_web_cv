from django.shortcuts import render

# Create your views here.
from .models import Profile, Skill, Experience, Project, Education, Language


def index(request):
    context = {
        'profile':     Profile.objects.first(),
        'hard_skills': Skill.objects.filter(category='hard'),
        'soft_skills': Skill.objects.filter(category='soft'),
        'experience':  Experience.objects.all()[:3],
        'education':   Education.objects.all(),
        'projects':    Project.objects.filter(featured=True),
        'languages':   Language.objects.all(),
    }
    return render(request, 'cv_editor/inicio.html', context)


def project_list(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'cv_editor/proyectos.html', context)
