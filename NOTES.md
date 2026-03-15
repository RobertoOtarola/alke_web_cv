# 🐍 CV Dinámico con Django — Rev. 3
**Revisión:** Senior Fullstack Architect  
**Módulo:** 6 — Desarrollo Web con Django (Alke Solutions / ABP)  
**Propósito:** Aplicación web Django para editar y renderizar un Curriculum Vitae dinámico, con referencia de UX en LinkedIn. Incluye diseño técnico, estructura de directorios, modelos ORM, backlog Scrumban y convenciones Git.

---

## Índice

1. [Fase 1 — Preguntas de Diseño](#fase-1--preguntas-de-diseño)
2. [Fase 2 — Diseño Técnico](#fase-2--diseño-técnico)
3. [Fase 3 — Backlog Scrumban (GitHub Projects)](#fase-3--backlog-scrumban-github-projects)
4. [Fase 4 — Hoja de Ruta de Construcción](#fase-4--hoja-de-ruta-de-construcción)
5. [Fase 5 — Convenciones Git](#fase-5--convenciones-git)

---

## Fase 1 — Preguntas de Diseño

### 🧠 Contenido

#### 1. ¿Qué información mostrará el CV?

| Sección | Campos clave | Cardinalidad |
|---|---|---|
| Datos personales | Nombre completo, título profesional, ubicación, LinkedIn, GitHub, foto | Único (`Profile`) |
| Perfil profesional | Bio / resumen ejecutivo | Único (`Profile.bio`) |
| Experiencia laboral | Empresa, cargo, fecha inicio / fin, logros | Lista (`Experience` + `Achievement`) |
| Educación | Título, institución, año de egreso | Lista (`Education`) |
| Habilidades | Nombre, categoría (hard / soft), nivel opcional | Lista (`Skill`) |
| Proyectos | Nombre, descripción técnica, stack, URL repositorio, destacado | Lista (`Project`) |
| Idiomas | Idioma, nivel (A1–C2 / nativo) | Lista (`Language`) |

> ✅ **Rev. 3:** Los logros de `Experience` se modelan como entidad separada (`Achievement`) con FK para evitar almacenar listas en texto plano. La foto migra a `ImageField` servido desde `MEDIA_ROOT`.

---

#### 2. ¿Qué secciones son dato único y cuáles son listas iterables?

- **Dato único (objeto singular):** `Profile` — agrupa datos personales, foto y bio. Se obtiene con `Profile.objects.first()`.
- **Listas / QuerySets:** `Experience`, `Achievement`, `Education`, `Skill`, `Project`, `Language`.

> ✅ **Rev. 3:** La terminología "lista de diccionarios" (Rev. 1) es incorrecta en contexto Django. Estos objetos son **QuerySets** del ORM, que permiten encadenamiento de filtros, paginación y acceso relacional desde el template (e.g., `{% for a in exp.achievements.all %}`).

---

#### 3. ¿Qué información se mostrará en la página principal (`/`)?

- **Hero Section:** nombre completo, título profesional y foto (desde `Profile`).
- **Resumen de habilidades:** Hard Skills destacadas (badges Bootstrap, filtradas por `category='hard'`).
- **Experiencia reciente:** los tres registros más recientes, ordenados por `start_date` descendente.
- **Proyectos destacados:** proyectos con `featured=True`.

> ✅ **Rev. 3:** El flag `featured` en `Project` permite controlar la visibilidad en Home sin duplicar lógica en el template.

---

### 🏗️ Estructura del Proyecto

#### 4. Nombre del proyecto y app

| Componente | Nombre | Razón |
|---|---|---|
| Proyecto Django | `roberto_portfolio` | Identifica el repositorio y el paquete de configuración |
| App principal | `cv_manager` | Encapsula modelos, vistas y lógica del CV |

---

#### 5. Páginas y rutas

| URL | Vista | Template | Descripción |
|---|---|---|---|
| `/` | `index` | `cv_manager/inicio.html` | CV completo renderizado (Home) |
| `/proyectos/` | `project_list` | `cv_manager/proyectos.html` | Galería detallada de proyectos |
| `/admin/` | Panel Django | — | Administración de datos (solo staff) |

---

#### 6. Bloques definidos en `base.html`

```html
{% block title %}{% endblock %}      {# Título de la pestaña del navegador #}
{% block extra_css %}{% endblock %}  {# Hojas de estilo específicas por vista #}
{% block content %}{% endblock %}    {# Cuerpo principal de cada página #}
{% block extra_js %}{% endblock %}   {# Scripts específicos por vista — al final del <body> #}
```

> ✅ **Rev. 3:** Se añade `{% block extra_js %}` al final del `<body>`. Es práctica estándar para cargar scripts específicos de cada vista sin contaminar el `base.html`.

---

#### 7. Archivos estáticos

```
static/
├── css/
│   └── custom.css         # Variables y sobrescritura de componentes Bootstrap
└── img/
    └── profile_photo.png  # Placeholder inicial (migrar a ImageField en producción)
```

> ✅ **Rev. 3:** A largo plazo, la foto de perfil debe gestionarse mediante `ImageField` en `Profile` y servirse desde `MEDIA_ROOT`. Los archivos en `static/` son assets de diseño (CSS, JS, íconos), no contenido dinámico del usuario.

---

### 🎨 Diseño Visual

#### 8. Paleta de colores (variables CSS / Bootstrap 5)

| Rol | Color | Hex | Uso |
|---|---|---|---|
| Primario | Azul corporativo | `#0d6efd` | Navbar, botones CTA, enlaces |
| Secundario | Verde éxito | `#198754` | Badges de Hard Skills |
| Fondo | Gris claro | `#f8f9fa` | Secciones alternas del CV |
| Texto | Gris oscuro | `#212529` | Cuerpo de texto general |

---

#### 9. Navegación

Navbar `sticky-top` con Bootstrap 5. Debe incluir:

- Enlace a Home (`/`)
- Enlace a Proyectos (`/proyectos/`)
- Enlace al panel Admin (`/admin/`) — visible solo para staff mediante `{% if request.user.is_staff %}`

> ✅ **Rev. 3:** La visibilidad condicional del enlace `/admin/` evita exponer la ruta de administración a visitantes anónimos.

---

#### 10. Framework CSS

Bootstrap 5 con grilla nativa (`col-*`). Enfoque mobile-first. Personalización mediante variables CSS en `custom.css`:

```css
:root {
  --bs-primary: #0d6efd;
  --bs-success: #198754;
}
```

---

## Fase 2 — Diseño Técnico

### Estructura de directorios completa

```
roberto_portfolio/                   ← Raíz del repositorio
├── .env                             ← Variables de entorno (NO versionar — agregar a .gitignore)
├── .gitignore
├── requirements.txt                 ← Dependencias del proyecto (django, pillow, python-decouple)
├── manage.py
│
├── roberto_portfolio/               ← Paquete de configuración Django
│   ├── __init__.py
│   ├── settings.py                  ← Configuración global (INSTALLED_APPS, STATIC, MEDIA, DB)
│   ├── urls.py                      ← Router principal (incluye cv_manager.urls y admin)
│   ├── wsgi.py
│   └── asgi.py
│
├── cv_manager/                      ← App principal
│   ├── migrations/                  ← Historial de cambios del esquema de BD
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py                     ← Registro de modelos en el panel de administración
│   ├── apps.py
│   ├── models.py                    ← Profile, Skill, Experience, Achievement, Education, Project, Language
│   ├── views.py                     ← index, project_list
│   └── urls.py                      ← Rutas locales de la app
│
├── templates/
│   ├── base.html                    ← Layout base con bloques title, extra_css, content, extra_js
│   └── cv_manager/
│       ├── inicio.html              ← Hero + Skills + Experiencia reciente + Proyectos destacados
│       └── proyectos.html           ← Galería completa de proyectos
│
├── static/
│   ├── css/
│   │   └── custom.css
│   └── img/
│       └── profile_photo.png        ← Placeholder (reemplazar con ImageField)
│
└── media/                           ← Archivos subidos por el usuario (ImageField, MEDIA_ROOT)
```

> ✅ **Rev. 3:** Se añaden `.env`, `python-decouple` y `asgi.py` como componentes estándar de un proyecto Django moderno. Las variables sensibles (`SECRET_KEY`, `DEBUG`) nunca se hardcodean en `settings.py`.

---

### Modelos (`cv_manager/models.py`)

```python
from django.db import models


class Profile(models.Model):
    full_name    = models.CharField(max_length=100)
    title        = models.CharField(max_length=150)       # "Fullstack Python Developer"
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
    end_date   = models.DateField(null=True, blank=True)  # null = trabajo actual

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Achievement(models.Model):
    """Logros asociados a una experiencia laboral (relación 1:N)."""
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
    stack       = models.CharField(max_length=200, blank=True)  # Ej: "Python, Django, Bootstrap"
    repo_url    = models.URLField(blank=True)
    featured    = models.BooleanField(default=False)            # Aparece en Home si True

    def __str__(self):
        return self.name


class Language(models.Model):
    name  = models.CharField(max_length=80)
    level = models.CharField(max_length=30)   # Ej: "C1 – Avanzado", "Nativo"

    def __str__(self):
        return f"{self.name} ({self.level})"
```

---

### Vistas (`cv_manager/views.py`)

```python
from django.shortcuts import render
from .models import Profile, Skill, Experience, Project, Education, Language


def index(request):
    context = {
        'profile':     Profile.objects.first(),
        'hard_skills': Skill.objects.filter(category='hard'),
        'soft_skills': Skill.objects.filter(category='soft'),
        'experience':  Experience.objects.all()[:3],      # 3 más recientes
        'education':   Education.objects.all(),
        'projects':    Project.objects.filter(featured=True),
        'languages':   Language.objects.all(),
    }
    return render(request, 'cv_manager/inicio.html', context)


def project_list(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'cv_manager/proyectos.html', context)
```

> ✅ **Rev. 3:** Se añaden `soft_skills`, `education` y `languages` al contexto de `index` para renderizar el CV completo en una sola vista, tal como lo hace LinkedIn. Los datos son QuerySets, no listas de diccionarios.

---

### Rutas (`cv_manager/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'cv_manager'

urlpatterns = [
    path('', views.index, name='index'),
    path('proyectos/', views.project_list, name='project-list'),
]
```

### Router principal (`roberto_portfolio/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cv_manager.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

### Registro en Admin (`cv_manager/admin.py`)

```python
from django.contrib import admin
from .models import Profile, Skill, Experience, Achievement, Education, Project, Language


class AchievementInline(admin.TabularInline):
    model = Achievement
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [AchievementInline]
    list_display = ('role', 'company', 'start_date', 'end_date')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'location')


admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Language)
```

> ✅ **Rev. 3:** Los `Achievement` se gestionan como inline dentro de `Experience` en el Admin, lo que refleja correctamente la relación 1:N y mejora la experiencia de edición.

---

### Configuración clave (`settings.py`)

```python
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

INSTALLED_APPS = [
    # ...
    'cv_manager',
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    # ...
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            # ...
        ],
    },
}]

STATIC_URL  = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'
```

---

## Fase 3 — Backlog Scrumban (GitHub Projects)

> **Metodología:** Scrumban — tablero Kanban continuo con cadencia de revisión semanal (sin sprints fijos). Las columnas son: `Backlog → Ready → In Progress → Review → Done`.

---

### 📋 EPIC 1 — Configuración del Entorno y Proyecto Base

**Objetivo:** Establecer el entorno de desarrollo reproducible y el scaffold del proyecto Django.

| ID | Tipo | Título | Criterios de aceptación | Etiquetas |
|---|---|---|---|---|
| T-01 | Task | Crear repositorio en GitHub con `.gitignore` Python/Django | Repo público, rama `main` protegida, `.gitignore` excluye `venv/`, `.env`, `__pycache__/`, `media/` | `setup`, `git` |
| T-02 | Task | Configurar entorno virtual e instalar dependencias | `venv` activo; `pip install django pillow python-decouple`; `requirements.txt` generado | `setup`, `backend` |
| T-03 | Task | Crear proyecto Django (`roberto_portfolio`) y verificar servidor | `django-admin startproject` exitoso; `runserver` responde en `localhost:8000` | `setup`, `backend` |
| T-04 | Task | Configurar variables de entorno con `python-decouple` | `.env` con `SECRET_KEY` y `DEBUG`; `settings.py` no contiene valores hardcodeados sensibles | `setup`, `security` |
| T-05 | Task | Crear app `cv_manager` y registrarla en `INSTALLED_APPS` | `startapp` ejecutado; app listada en `settings.py`; estructura de archivos verificada | `setup`, `backend` |

---

### 📋 EPIC 2 — Modelos y Base de Datos

**Objetivo:** Definir el esquema de datos del CV como modelos Django y aplicarlo a la base de datos SQLite.

| ID | Tipo | Título | Criterios de aceptación | Etiquetas |
|---|---|---|---|---|
| T-06 | Task | Implementar modelo `Profile` | Campos: `full_name`, `title`, `bio`, `location`, `linkedin_url`, `github_url`, `photo` (ImageField) | `backend`, `models` |
| T-07 | Task | Implementar modelos `Experience` y `Achievement` | `Achievement` con FK a `Experience`; `related_name='achievements'`; Meta `ordering` configurado | `backend`, `models` |
| T-08 | Task | Implementar modelos `Education`, `Skill`, `Project`, `Language` | Todos los campos definidos según especificación; `Project.featured` con default `False` | `backend`, `models` |
| T-09 | Task | Generar y aplicar migraciones | `makemigrations` y `migrate` sin errores; esquema verificado en SQLite | `backend`, `database` |
| T-10 | Task | Registrar modelos en `admin.py` con `AchievementInline` | Panel `/admin/` muestra todos los modelos; `Achievement` editable inline dentro de `Experience` | `backend`, `admin` |
| T-11 | Task | Crear superusuario y poblar datos de prueba | `createsuperuser` ejecutado; al menos un `Profile`, dos `Experience` con logros, tres `Skill`, dos `Project` cargados | `backend`, `admin` |

---

### 📋 EPIC 3 — Vistas y Enrutamiento

**Objetivo:** Implementar las vistas Django que construyen el contexto de datos y las rutas que las exponen.

| ID | Tipo | Título | Criterios de aceptación | Etiquetas |
|---|---|---|---|---|
| T-12 | Task | Implementar vista `index` con contexto completo | Contexto incluye: `profile`, `hard_skills`, `soft_skills`, `experience` (3 recientes), `education`, `projects` (featured), `languages` | `backend`, `views` |
| T-13 | Task | Implementar vista `project_list` | Contexto incluye todos los `Project`; ordenados por nombre o fecha | `backend`, `views` |
| T-14 | Task | Configurar URLs de la app (`cv_manager/urls.py`) | Rutas `/` y `/proyectos/` definidas con `app_name = 'cv_manager'`; `name` asignado a cada URL | `backend`, `routing` |
| T-15 | Task | Configurar router principal e integrar rutas de `MEDIA` | `roberto_portfolio/urls.py` incluye `cv_manager.urls`, `admin` y `static(MEDIA_URL, ...)` | `backend`, `routing` |

---

### 📋 EPIC 4 — Templates y Archivos Estáticos

**Objetivo:** Construir la capa de presentación HTML/CSS con Bootstrap 5 y el sistema de templates de Django.

| ID | Tipo | Título | Criterios de aceptación | Etiquetas |
|---|---|---|---|---|
| T-16 | Task | Crear `base.html` con navbar, bloques y Bootstrap 5 CDN | Cuatro bloques definidos; navbar sticky con enlace condicional `/admin/`; `{% load static %}` presente | `frontend`, `templates` |
| T-17 | Task | Implementar `inicio.html` — sección Hero | Muestra `profile.full_name`, `profile.title`, `profile.photo`; extiende `base.html` | `frontend`, `templates` |
| T-18 | Task | Implementar `inicio.html` — sección Habilidades | Hard Skills como badges Bootstrap (`bg-success`); Soft Skills como badges secundarios | `frontend`, `templates` |
| T-19 | Task | Implementar `inicio.html` — sección Experiencia | Loop `{% for exp in experience %}` con logros anidados `{% for a in exp.achievements.all %}` | `frontend`, `templates` |
| T-20 | Task | Implementar `inicio.html` — secciones Educación, Idiomas y Proyectos destacados | Cada sección con loop correspondiente; proyectos con `repo_url` condicional | `frontend`, `templates` |
| T-21 | Task | Crear `proyectos.html` con galería de proyectos | Cards Bootstrap con nombre, descripción, stack y enlace al repositorio (si existe) | `frontend`, `templates` |
| T-22 | Task | Configurar archivos estáticos y `custom.css` | `STATIC_URL` y `STATICFILES_DIRS` en `settings.py`; `custom.css` con variables CSS cargado en `base.html` | `frontend`, `static` |

---

### 📋 EPIC 5 — Calidad, Documentación y Entrega

**Objetivo:** Asegurar que el proyecto sea reproducible, documentado y listo para presentación.

| ID | Tipo | Título | Criterios de aceptación | Etiquetas |
|---|---|---|---|---|
| T-23 | Task | Verificar flujo completo en servidor de desarrollo | `runserver` sin errores; `/`, `/proyectos/` y `/admin/` responden correctamente; imágenes de Media visibles | `qa`, `testing` |
| T-24 | Task | Redactar `README.md` con instrucciones de instalación | Incluye: clonar repo, crear venv, instalar dependencias, configurar `.env`, aplicar migraciones, crear superusuario, ejecutar servidor | `docs` |
| T-25 | Task | Tomar capturas de pantalla del proyecto en ejecución | Al menos 3 capturas: Home, Proyectos y panel Admin; incluidas en el documento entregable | `docs`, `delivery` |
| T-26 | Task | Comprimir el proyecto en `.zip` para entrega | Excluir `venv/`, `media/`, `__pycache__/` y `.env`; `.zip` verificado con extracción limpia | `delivery` |
| T-27 | Task | Redactar documento explicativo (PDF/DOCX) | Describe estructura de carpetas, flujo petición-respuesta y capturas de pantalla | `docs`, `delivery` |

---

## Fase 4 — Hoja de Ruta de Construcción

| # | Paso | Comando / Acción |
|---|---|---|
| 1 | Crear repositorio GitHub | Inicializar con `.gitignore` Python; clonar localmente |
| 2 | Crear entorno virtual | `python -m venv venv && source venv/bin/activate` (Linux/Mac) / `venv\Scripts\activate` (Windows) |
| 3 | Instalar dependencias | `pip install django pillow python-decouple` |
| 4 | Generar `requirements.txt` | `pip freeze > requirements.txt` |
| 5 | Crear proyecto Django | `django-admin startproject roberto_portfolio .` |
| 6 | Crear app | `python manage.py startapp cv_manager` |
| 7 | Configurar `.env` | Crear `.env` con `SECRET_KEY` y `DEBUG=True`; actualizar `settings.py` con `decouple` |
| 8 | Registrar app | Añadir `'cv_manager'` a `INSTALLED_APPS` en `settings.py` |
| 9 | Definir modelos | Implementar clases en `cv_manager/models.py` |
| 10 | Crear y aplicar migraciones | `python manage.py makemigrations && python manage.py migrate` |
| 11 | Registrar en Admin | Configurar `cv_manager/admin.py` con `@admin.register` e inline |
| 12 | Crear superusuario | `python manage.py createsuperuser` |
| 13 | Configurar rutas | Definir `cv_manager/urls.py` e incluirlo en `roberto_portfolio/urls.py` |
| 14 | Implementar vistas | Funciones `index` y `project_list` en `views.py` con contextos completos |
| 15 | Configurar templates y estáticos | `DIRS`, `STATIC_URL`, `STATICFILES_DIRS`, `MEDIA_URL`, `MEDIA_ROOT` en `settings.py` |
| 16 | Construir templates | `base.html` con bloques + `inicio.html` + `proyectos.html` con loops `{% for %}` |
| 17 | Poblar datos | Ingresar al panel `/admin/` y cargar perfil, habilidades, experiencia y proyectos |
| 18 | Verificar en desarrollo | `python manage.py runserver` → verificar `/`, `/proyectos/`, `/admin/` |

---

## Fase 5 — Convenciones Git

### Estrategia de ramas

```
main          ← rama de producción / entrega final (protegida)
develop       ← integración continua de features
feature/*     ← una rama por cada Task del backlog
fix/*         ← correcciones de bugs
```

### Formato de commit (Conventional Commits)

```
<tipo>(<scope>): <descripción imperativa en presente>

Ejemplos:
feat(models): add Achievement model with FK to Experience
feat(views): include languages and education in index context
fix(admin): register Language model in admin site
style(templates): add Bootstrap badges for hard skills section
docs(readme): add installation and setup instructions
chore(deps): add python-decouple to requirements.txt
```

### Flujo de trabajo por Task

```bash
# 1. Crear rama desde develop
git checkout develop
git pull origin develop
git checkout -b feature/T-06-model-profile

# 2. Implementar la tarea
# ... editar archivos ...

# 3. Commit con mensaje semántico
git add cv_manager/models.py
git commit -m "feat(models): add Profile model with ImageField"

# 4. Push y abrir Pull Request hacia develop
git push origin feature/T-06-model-profile
# Abrir PR en GitHub → asignar revisor → merge tras aprobación

# 5. Merge y cierre del Task en GitHub Projects
```

### `.gitignore` esencial

```
venv/
.env
__pycache__/
*.pyc
*.pyo
db.sqlite3
media/
staticfiles/
*.zip
.DS_Store
```

---

*Documento generado bajo criterios de arquitectura Django estándar (v4.x+), metodología Scrumban y Conventional Commits. Revisión: Senior Fullstack Architect.*
