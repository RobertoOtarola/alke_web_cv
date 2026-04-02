from django.shortcuts import render, get_object_or_404

from .models import Project, CaseStudy


def portfolio_index(request):
    """Main portfolio view: shows both featured and other project cards."""
    proyectos_destacados = Project.objects.filter(destacado=True).order_by('orden')
    otros_proyectos = Project.objects.filter(destacado=False).order_by('orden')
    
    context = {
        'proyectos': proyectos_destacados,
        'otros_proyectos': otros_proyectos,
    }
    return render(request, 'portfolio/index.html', context)


def case_study_detail(request, slug):
    """Detailed case study view."""
    case_study = get_object_or_404(CaseStudy, slug=slug)
    return render(request, 'portfolio/case_study.html', {'case_study': case_study})
