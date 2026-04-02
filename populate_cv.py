"""
populate_cv.py
──────────────
Script de carga inicial de datos del CV en la base de datos.

Uso:
    python populate_cv.py          # carga local (SQLite)
    DJANGO_SETTINGS_MODULE=config.settings.production python populate_cv.py

⚠️  En producción solicita confirmación antes de borrar datos.
"""

import os
import sys
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

import django  # noqa: E402
django.setup()

from apps.cv.models import (  # noqa: E402
    Achievement, Education, Experience, Language, Profile, Project, Skill
)


def confirm_if_production() -> None:
    """Detiene la ejecución en producción si el usuario no confirma (CR-26)."""
    settings_module = os.environ.get("DJANGO_SETTINGS_MODULE", "")
    if "production" in settings_module:
        print("⚠️  Estás conectado a la base de datos de PRODUCCIÓN (Supabase).")
        print("    Esto borrará TODOS los datos existentes.")
        confirm = input("    Escribe 'SI' para continuar: ").strip()
        if confirm != "SI":
            print("Cancelado.")
            sys.exit(0)


def run() -> None:
    """Ejecuta la carga completa de datos del CV."""
    confirm_if_production()

    print("Limpiando datos existentes...")
    Profile.objects.all().delete()
    Skill.objects.all().delete()
    Experience.objects.all().delete()
    Education.objects.all().delete()
    Project.objects.all().delete()
    Language.objects.all().delete()

    print("Creando Profile...")
    Profile.objects.create(
        full_name="Roberto Alexandre Otárola Estrada",
        title="Desarrollador Fullstack Python Trainee | Energías Renovables",
        bio=(
            "Gerente senior con más de 18 años de experiencia en energías renovables, "
            "actualmente en transición hacia el desarrollo de software fullstack con Python y Django."
        ),
        location="Santiago, Chile",
        email="roberto.otarola@yahoo.com",
        linkedin_url="https://www.linkedin.com/in/robertootarola/",
        github_url="https://github.com/RobertoOtarola",
    )

    print("Creando Skills...")
    hard_skills = [
        "Python", "Django", "SQL", "PostgreSQL",
        "Supabase", "Git", "GitHub", "Bootstrap",
        "Energía Solar Fotovoltaica (FV)", "PVsyst", "NREL SAM",
    ]
    soft_skills = [
        "Gestión de Proyectos", "Liderazgo de Equipos",
        "Comunicación Técnica", "Aprendizaje Continuo",
        "Trabajo en Equipo", "Pensamiento Estratégico",
    ]
    for name in hard_skills:
        Skill.objects.create(name=name, category="hard")
    for name in soft_skills:
        Skill.objects.create(name=name, category="soft")

    print("Creando Experiences...")
    exp1 = Experience.objects.create(
        company="AUTOENERGIAS",
        role="Product Manager – Energías Renovables",
        location="Santiago, Chile",
        start_date=date(2025, 6, 1),
        featured=True,
    )
    Achievement.objects.create(
        experience=exp1,
        description=(
            "Lideré el diseño conceptual de sistemas solares FV, incrementando la cartera de "
            "proyectos mediante estrategias de ventas B2C y B2B."
        ),
    )
    Achievement.objects.create(
        experience=exp1,
        description=(
            "Implementé campañas de marketing digital y desarrollo web orientadas a "
            "posicionamiento de marca en el segmento de energía solar y baterías."
        ),
    )

    exp2 = Experience.objects.create(
        company="SOSTENER",
        role="Cofundador y Administrador",
        location="Santiago, Chile",
        start_date=date(2013, 7, 1),
        featured=True,
    )
    Achievement.objects.create(
        experience=exp2,
        description=(
            "Fundé y administré empresa de ingeniería sostenible, diseñando modelos de negocio "
            "y gestionando proyectos de energía renovable para clientes corporativos."
        ),
    )

    exp3 = Experience.objects.create(
        company="ASTRONERGY",
        role="Gerente de Servicio Técnico para Latinoamérica",
        location="Santiago, Chile",
        start_date=date(2023, 3, 1),
        end_date=date(2023, 11, 30),
        featured=True,
    )
    Achievement.objects.create(
        experience=exp3,
        description=(
            "Representé a fabricante líder de módulos FV ante clientes en toda Latinoamérica, "
            "gestionando comunicaciones técnicas internacionales con la casa matriz en China."
        ),
    )

    print("Creando Education...")
    Education.objects.create(
        degree="Magíster en Ingeniería de la Energía",
        institution="Pontificia Universidad Católica de Chile",
        start_year=2008,
        year=2014,
    )
    Education.objects.create(
        degree="Ingeniero Comercial, mención Economía",
        institution="Universidad de Chile",
        start_year=1998,
        year=2004,
    )

    print("Creando Projects...")
    Project.objects.create(
        name="alke_web_cv — CV Web Dinámico",
        description=(
            "Aplicación web Django que renderiza el CV dinámicamente desde PostgreSQL (Supabase), "
            "desplegada en Render con dominio personalizado vía Cloudflare."
        ),
        stack="Python · Django 5.2 · PostgreSQL · Supabase · Render · WhiteNoise · Gunicorn",
        repo_url="https://github.com/RobertoOtarola/alke_web_cv",
        featured=True,
    )

    print("Creando Languages...")
    Language.objects.create(name="Español", level="Nativo")
    Language.objects.create(name="Inglés", level="TOEIC Avanzado (2+)")
    Language.objects.create(name="Portugués", level="Intermedio")

    print("✅ Base de datos poblada correctamente.")


if __name__ == "__main__":
    run()
