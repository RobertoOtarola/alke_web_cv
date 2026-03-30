import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from apps.cv.models import Profile, Skill, Experience, Achievement, Education, Project, Language

def run():
    print("Clearing old data...")
    Profile.objects.all().delete()
    Skill.objects.all().delete()
    Experience.objects.all().delete()
    Education.objects.all().delete()
    Project.objects.all().delete()
    Language.objects.all().delete()

    print("Creating Profile...")
    profile = Profile.objects.create(
        full_name="Roberto Alexandre Otárola Estrada",
        title="Gerente senior en la industria de energías renovables",
        bio="Gerente senior con más de 18 años de experiencia en la industria de energías renovables, especializado en energía solar fotovoltaica (FV) y concentración solar de potencia (CSP). Doble formación en Ingeniería Comercial (Economía) y Magíster en Ingeniería de la Energía (PUC).",
        location="Santiago, Chile",
        linkedin_url="https://www.linkedin.com/in/robertootarola/"
    )

    print("Creating Skills...")
    skills = [
        ("Energía Solar Fotovoltaica (FV)", "hard"),
        ("Concentración Solar de Potencia (CSP)", "hard"),
        ("Sistemas de Almacenamiento de Energía (BESS)", "hard"),
        ("Ingeniería Conceptual", "hard"),
        ("PVsyst", "hard"),
        ("Desarrollo de Negocios B2B y B2C", "soft"),
        ("Gerenciamiento de Proyectos", "soft"),
        ("Planificación Estratégica", "soft"),
        ("Liderazgo de Equipos", "soft"),
    ]
    for s_name, s_cat in skills:
        Skill.objects.create(name=s_name, category=s_cat)

    print("Creating Experiences & Achievements...")
    
    # Autoenergias
    exp1 = Experience.objects.create(
        company="AUTOENERGIAS — Energía Solar y Baterías",
        role="Product Manager – Energías Renovables",
        start_date=date(2025, 6, 1)
    )
    Achievement.objects.create(experience=exp1, description="Lideré el diseño conceptual de sistemas solares fotovoltaicos residenciales e industriales.")
    Achievement.objects.create(experience=exp1, description="Implementé campañas de marketing digital y desarrollo web orientadas a posicionamiento de marca.")

    # Sostener
    exp2 = Experience.objects.create(
        company="SOSTENER — Diseño e Ingeniería Sostenible",
        role="Cofundador y Administrador",
        start_date=date(2013, 7, 1)
    )
    Achievement.objects.create(experience=exp2, description="Fundé y administré empresa de ingeniería sostenible, diseñando modelos de negocio innovadores.")

    print("Creating Educations...")
    Education.objects.create(
        degree="Magíster en Ingeniería de la Energía",
        institution="Pontificia Universidad Católica de Chile",
        year=2014
    )
    Education.objects.create(
        degree="Ingeniero Comercial, mención Economía",
        institution="Universidad de Chile",
        year=2004
    )

    print("Creating Languages...")
    Language.objects.create(name="Español", level="Nativo")
    Language.objects.create(name="Inglés", level="TOEIC Trabajo Avanzado 2+")
    Language.objects.create(name="Portugués", level="Intermedio")

    print("Done! DB populated.")

if __name__ == '__main__':
    run()
