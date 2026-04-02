from django.test import TestCase
from django.urls import reverse

class PortfolioViewsTestCase(TestCase):
    """Básicos tests de carga para las vistas del portafolio."""

    def test_portfolio_index_loads(self):
        response = self.client.get(reverse('portfolio:index'))
        self.assertEqual(response.status_code, 200)

    def test_projects_redirect_works(self):
        # La ruta antigua /portfolio/proyectos/ debe redirigir (301) a /portfolio/
        response = self.client.get(reverse('portfolio:proyectos_redirect'))
        self.assertEqual(response.status_code, 301)
        self.assertIn(reverse('portfolio:index'), response.url)

    def test_health_check_loads(self):
        response = self.client.get(reverse('health'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "ok")
