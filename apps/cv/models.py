from django.db import models

# Create your models here.
class Profile(models.Model):
    full_name    = models.CharField(max_length=100)
    title        = models.CharField(max_length=150)
    bio          = models.TextField()
    location     = models.CharField(max_length=100)
    linkedin_url = models.URLField(blank=True)
    github_url   = models.URLField(blank=True)
    photo        = models.ImageField(upload_to='profile/', blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [('hard', 'Hard Skill'), ('soft', 'Soft Skill')]
    name     = models.CharField(max_length=80)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.category})"


class Experience(models.Model):
    company    = models.CharField(max_length=150)
    role       = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date   = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Achievement(models.Model):
    experience  = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='achievements'
    )
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description[:60]


class Education(models.Model):
    degree      = models.CharField(max_length=150)
    institution = models.CharField(max_length=150)
    year        = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Project(models.Model):
    name        = models.CharField(max_length=150)
    description = models.TextField()
    stack       = models.CharField(max_length=200, blank=True)
    repo_url    = models.URLField(blank=True)
    featured    = models.BooleanField(default=False)

    @property
    def stack_list(self):
        """Return stack as a list of trimmed technology names."""
        if self.stack:
            return [tech.strip() for tech in self.stack.split(',') if tech.strip()]
        return []

    def __str__(self):
        return self.name


class Language(models.Model):
    name  = models.CharField(max_length=80)
    level = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} ({self.level})"
