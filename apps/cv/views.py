from django.shortcuts import render
from django.utils import timezone

from .models import Profile, Skill, Experience, Education, Language, Project
from apps.portfolio.models import Proyecto


def index(request):
    """
    Vista principal del CV.

    Renderiza 503 si la base de datos no tiene datos de perfil cargados,
    evitando un AttributeError en el template (CR-15).
    """
    profile = Profile.objects.first()
    if profile is None:
        return render(request, "cv/sin_datos.html", status=503)

    experience_qs = Experience.objects.prefetch_related("achievements").all()

    # Estadísticas dinámicas para el counter bar
    earliest_exp = experience_qs.order_by("start_date").first()
    years_experience = 0
    if earliest_exp:
        years_experience = timezone.now().year - earliest_exp.start_date.year

    stats = {
        "years_experience": years_experience,
        "total_projects":   Proyecto.objects.count(),
        "total_skills":     Skill.objects.count(),
        "total_languages":  Language.objects.count(),
    }

    context = {
        "profile":     profile,
        "hard_skills": Skill.objects.filter(category="hard"),
        "soft_skills": Skill.objects.filter(category="soft"),
        # CR-14: prefetch_related resuelve el N+1 — una sola query extra para
        # todos los achievements, en lugar de una query por experiencia.
        # CR-16: se muestran solo las experiencias marcadas como destacadas;
        # si no hay ninguna, se toman las 3 más recientes como fallback.
        "experience": (
            Experience.objects.prefetch_related("achievements").filter(featured=True)
            or Experience.objects.prefetch_related("achievements").all()[:3]
        ),
        "education":  Education.objects.all(),
        "projects":   Project.objects.filter(featured=True),
        "languages":  Language.objects.all(),
        "stats":      stats,
    }
    return render(request, "cv/index.html", context)


def project_list(request):
    """Vista con el listado completo de proyectos, destacados primero (CR-17)."""
    context = {
        "projects": Project.objects.order_by("-featured", "name"),
    }
    return render(request, "cv/proyectos.html", context)
