from django.test import TestCase
from django.urls import reverse

class PortfolioViewsTestCase(TestCase):
    """Básicos tests de carga para las vistas del portafolio."""

    def test_landing_page_loads(self):
        response = self.client.get(reverse('portfolio:landing'))
        self.assertEqual(response.status_code, 200)

    def test_projects_gallery_loads(self):
        response = self.client.get(reverse('portfolio:project-list'))
        self.assertEqual(response.status_code, 200)

    def test_health_check_loads(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "ok")
