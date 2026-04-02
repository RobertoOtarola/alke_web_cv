from django.db import models

class Project(models.Model):
    nombre      = models.CharField(max_length=200, db_index=True)
    descripcion = models.TextField()
    tecnologias = models.CharField(max_length=500, blank=True, null=True)
    url_repositorio = models.URLField(blank=True, null=True)
    url_demo    = models.URLField(blank=True, null=True)
    imagen_url  = models.URLField(
        blank=True,
        null=True,
        help_text="URL absoluta de la imagen del proyecto (GitHub Pages u otro CDN)."
    )
    destacado   = models.BooleanField(default=False, db_index=True)
    orden       = models.PositiveSmallIntegerField(default=0)
    fecha_creacion = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["orden", "-fecha_creacion"]
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.nombre


class CaseStudy(models.Model):
    """Detailed case study linked to a featured project."""

    proyecto = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='case_study',
    )
    slug = models.SlugField(max_length=120, unique=True)
    subtitle = models.CharField(
        max_length=255,
        help_text='Lead text shown below the title.',
    )
    image = models.ImageField(
        upload_to='portfolio/case_studies/',
        blank=True,
        help_text='Preview image for the case study header.',
    )
    skills_applied = models.CharField(
        max_length=500,
        blank=True,
        help_text='Comma-separated skill tags (e.g. "Fullstack, DevOps, Git").',
    )

    # 8 sections from the original case-study.html
    section_1_description = models.TextField(
        verbose_name='1. Breve descripción de la actividad',
        blank=True,
    )
    section_2_challenge = models.TextField(
        verbose_name='2. Desafío principal',
        blank=True,
    )
    section_3_solution = models.TextField(
        verbose_name='3. Solución propuesta',
        blank=True,
    )
    section_4_tools = models.TextField(
        verbose_name='4. Herramientas técnicas utilizadas',
        blank=True,
    )
    section_5_learnings = models.TextField(
        verbose_name='5. Principales aprendizajes',
        blank=True,
    )
    section_6_metrics = models.TextField(
        verbose_name='6. Métricas de impacto',
        blank=True,
    )
    section_7_skills = models.TextField(
        verbose_name='7. Habilidades técnicas aplicadas',
        blank=True,
    )
    section_8_justification = models.TextField(
        verbose_name='8. Justificación de la elección',
        blank=True,
    )

    class Meta:
        verbose_name = 'Caso de Estudio'
        verbose_name_plural = 'Casos de Estudio'

    def __str__(self):
        return f'Caso de Estudio: {self.proyecto.nombre}'

    @property
    def skills_list(self):
        """Return skills_applied as a list of trimmed strings."""
        if self.skills_applied:
            return [s.strip() for s in self.skills_applied.split(',') if s.strip()]
        return []
