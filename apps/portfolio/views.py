from django.shortcuts import render, get_object_or_404

from .models import Proyecto, CaseStudy


def portfolio_index(request):
    """Main portfolio view: shows featured project cards."""
    proyectos = Proyecto.objects.filter(destacado=True).order_by('orden')
    return render(request, 'portfolio/index.html', {'proyectos': proyectos})


def case_study_detail(request, slug):
    """Detailed case study view."""
    case_study = get_object_or_404(CaseStudy, slug=slug)
    return render(request, 'portfolio/case_study.html', {'case_study': case_study})
