from django.shortcuts import render
from django.utils import timezone

from .models import Profile, Skill, Experience, Education, Language
from apps.portfolio.models import Proyecto

def index(request):
    """Home page: full CV with all sections + computed stats + CTA to portfolio."""
    experience_qs = Experience.objects.all()

    # Compute dynamic stats for the counter bar
    earliest_exp = experience_qs.order_by('start_date').first()
    years_experience = 0
    if earliest_exp:
        years_experience = timezone.now().year - earliest_exp.start_date.year

    stats = {
        'years_experience': years_experience,
        'total_projects':   Proyecto.objects.count(),
        'total_skills':     Skill.objects.count(),
        'total_languages':  Language.objects.count(),
    }

    context = {
        'profile':     Profile.objects.first(),
        'hard_skills': Skill.objects.filter(category='hard'),
        'soft_skills': Skill.objects.filter(category='soft'),
        'experience':  experience_qs[:3],
        'education':   Education.objects.all(),
        'languages':   Language.objects.all(),
        'stats':       stats,
    }
    return render(request, 'cv/index.html', context)
