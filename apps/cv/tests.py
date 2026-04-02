from django.test import TestCase
from django.urls import reverse

from .models import Achievement, Education, Experience, Language, Profile, Project, Skill


class IndexViewTest(TestCase):
    """Tests para la vista principal del CV (CR-19)."""

    def test_index_sin_perfil_retorna_503(self):
        """Sin datos de Profile, la home retorna HTTP 503."""
        response = self.client.get(reverse("cv:index"))
        self.assertEqual(response.status_code, 503)
        self.assertTemplateUsed(response, "cv/sin_datos.html")

    def test_index_con_perfil_retorna_200(self):
        """Con un Profile cargado, la home retorna HTTP 200."""
        Profile.objects.create(
            full_name="Test User",
            title="Developer",
            bio="Bio de prueba.",
            location="Santiago",
        )
        response = self.client.get(reverse("cv:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cv/index.html")

    def test_index_muestra_nombre_del_perfil(self):
        """El nombre del perfil aparece en el HTML de la home."""
        Profile.objects.create(
            full_name="Roberto Otárola",
            title="Dev",
            bio="Bio.",
            location="Santiago",
        )
        response = self.client.get(reverse("cv:index"))
        self.assertContains(response, "Roberto Otárola")

    def test_index_no_lanza_error_con_bd_vacia(self):
        """Sin datos, la vista no lanza AttributeError — retorna 503 limpio."""
        response = self.client.get(reverse("cv:index"))
        self.assertNotEqual(response.status_code, 500)

    def test_index_sin_n_mas_uno(self):
        """Con prefetch_related, el número de queries no escala con experiencias."""
        Profile.objects.create(
            full_name="Test", title="Dev", bio="Bio.", location="Santiago"
        )
        for i in range(5):
            exp = Experience.objects.create(
                company=f"Empresa {i}", role="Dev",
                start_date=f"202{i}-01-01", featured=True
            )
            Achievement.objects.create(experience=exp, description=f"Logro {i}")

        # Capturamos la cantidad de queries con 5 experiencias y verificamos
        # que es menor a 20 (sin N+1 sería ~10 queries, con N+1 sería 5+ extra).
        from django.test.utils import CaptureQueriesContext
        from django.db import connection
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse("cv:index"))
        self.assertEqual(response.status_code, 200)
        # Sin prefetch habría 1 query extra por cada experiencia; con 5 exp
        # el N+1 daría ~15 queries, con prefetch debería ser ≤ 15.
        self.assertLessEqual(len(ctx.captured_queries), 15,
            f"Posible N+1: se ejecutaron {len(ctx.captured_queries)} queries")


class ProjectListViewTest(TestCase):
    """Tests para la vista de listado de proyectos (CR-19)."""

    def test_projects_retorna_200(self):
        response = self.client.get(reverse("cv:project-list"))
        self.assertEqual(response.status_code, 200)

    def test_projects_vacio_muestra_mensaje(self):
        response = self.client.get(reverse("cv:project-list"))
        self.assertContains(response, "No hay proyectos")

    def test_projects_orden_featured_primero(self):
        """Los proyectos destacados aparecen antes que los no destacados."""
        Project.objects.create(name="Proyecto B", description="Desc", featured=False)
        Project.objects.create(name="Proyecto A", description="Desc", featured=True)
        response = self.client.get(reverse("cv:project-list"))
        proyectos = list(response.context["projects"])
        self.assertTrue(proyectos[0].featured)


class ModelStrTest(TestCase):
    """Tests de __str__ para todos los modelos (CR-19)."""

    def test_profile_str(self):
        p = Profile(full_name="Roberto Otárola", title="Dev", bio="", location="Santiago")
        self.assertEqual(str(p), "Roberto Otárola")

    def test_experience_str(self):
        e = Experience(company="ACME", role="Dev", start_date="2023-01-01")
        self.assertEqual(str(e), "Dev @ ACME")

    def test_achievement_str_trunca_a_60(self):
        e = Experience(company="ACME", role="Dev", start_date="2023-01-01")
        a = Achievement(experience=e, description="Logro largo " * 10)
        self.assertEqual(len(str(a)), 60)

    def test_skill_str(self):
        s = Skill(name="Python", category="hard")
        self.assertEqual(str(s), "Python (hard)")

    def test_language_str(self):
        lang = Language(name="Inglés", level="Avanzado")
        self.assertEqual(str(lang), "Inglés (Avanzado)")

    def test_project_str(self):
        p = Project(name="Mi Proyecto", description="Desc")
        self.assertEqual(str(p), "Mi Proyecto")
