from django.db import models


class Profile(models.Model):
    """Datos personales y de contacto del titular del CV."""

    full_name    = models.CharField(max_length=100)
    title        = models.CharField(max_length=150)
    bio          = models.TextField()
    location     = models.CharField(max_length=100)
    email        = models.EmailField(blank=True)          # CR-13: campo añadido
    linkedin_url = models.URLField(blank=True)
    github_url   = models.URLField(blank=True)
    photo        = models.ImageField(upload_to="profile/", blank=True)

    def __str__(self) -> str:
        return self.full_name


class Skill(models.Model):
    """Habilidad técnica (hard) o blanda (soft)."""

    CATEGORY_CHOICES = [("hard", "Hard Skill"), ("soft", "Soft Skill")]

    name     = models.CharField(max_length=80)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"


class Experience(models.Model):
    """Experiencia laboral con sus logros asociados."""

    company    = models.CharField(max_length=150)
    role       = models.CharField(max_length=150)
    location   = models.CharField(max_length=100, blank=True)   # CR-10
    start_date = models.DateField()
    end_date   = models.DateField(null=True, blank=True)
    featured   = models.BooleanField(default=False)              # CR-11

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return f"{self.role} @ {self.company}"


class Achievement(models.Model):
    """Logro o responsabilidad dentro de una experiencia laboral."""

    experience  = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name="achievements"
    )
    description = models.TextField()   # CR-09: CharField(500) → TextField

    def __str__(self) -> str:
        return self.description[:60]


class Education(models.Model):
    """Formación académica."""

    degree      = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    start_year  = models.PositiveSmallIntegerField(null=True, blank=True)  # CR-12
    year        = models.PositiveSmallIntegerField(verbose_name="Año de término")

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return f"{self.degree} — {self.institution}"




class Language(models.Model):
    """Idioma y nivel de dominio."""

    name  = models.CharField(max_length=80)
    level = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name} ({self.level})"


class Certification(models.Model):
    """Certificación profesional."""

    year        = models.PositiveSmallIntegerField()
    name        = models.CharField(max_length=200)
    institution = models.CharField(max_length=150)

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return f"{self.name} ({self.year})"


class Publication(models.Model):
    """Publicación técnica o académica."""

    publication_type = models.CharField(max_length=50)
    title            = models.CharField(max_length=255)
    event            = models.CharField(max_length=200)
    year             = models.PositiveSmallIntegerField()
    role             = models.CharField(max_length=100)

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return self.title


class Presentation(models.Model):
    """Presentación en evento o congreso."""

    event    = models.CharField(max_length=200)
    location = models.CharField(max_length=150)
    year     = models.PositiveSmallIntegerField()
    topic    = models.CharField(max_length=255)

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return self.event
