from django.shortcuts import render, get_object_or_404

from apps.cv.models import Profile, Project
from .models import CaseStudy


def landing(request):
    """Portfolio landing page: hero + featured project cards."""
    context = {
        'profile':  Profile.objects.first(),
        'projects': Project.objects.filter(featured=True),
    }
    return render(request, 'portfolio/landing.html', context)


def project_list(request):
    """Full project gallery (migrated from cv app)."""
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'portfolio/projects.html', context)


def case_study_detail(request, slug):
    """Render a single case study by slug."""
    case_study = get_object_or_404(CaseStudy, slug=slug)
    context = {
        'case_study': case_study,
    }
    return render(request, 'portfolio/case_study.html', context)
