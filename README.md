# 🐍 CV Dinámico con Django

**Bootcamp Desarrollo de Aplicaciones Fullstack Python Trainee | Módulo #6 | ABP**

Aplicación web Django para editar y renderizar un Curriculum Vitae dinámico, con referencia de UX en LinkedIn. Permite gestionar secciones del CV (perfil, experiencia, habilidades, proyectos, educación e idiomas) desde el panel de administración de Django.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tech Stack](#-tech-stack)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Modelos de Datos](#-modelos-de-datos)
- [Convenciones Git](#-convenciones-git)

---

## ✨ Características

- **CV completo en una sola página** — Hero, habilidades, experiencia reciente, educación, idiomas y proyectos destacados.
- **Galería de proyectos** — Página dedicada con todos los proyectos y enlaces a repositorios.
- **Panel de administración** — Gestión de contenido vía Django Admin con `AchievementInline` para logros.
- **Diseño responsive** — Bootstrap 5 con enfoque mobile-first.
- **Variables de entorno** — Configuración segura con `python-decouple` (`.env`).
- **Archivos multimedia** — Soporte para foto de perfil vía `ImageField` y `MEDIA_ROOT`.

---

## 🛠 Tech Stack

| Tecnología | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| Django 4.x+ | Framework web |
| Bootstrap 5 | Framework CSS (CDN) |
| SQLite | Base de datos (desarrollo) |
| Pillow | Procesamiento de imágenes (`ImageField`) |
| python-decouple | Variables de entorno |

---

## 📁 Estructura del Proyecto

```
roberto_portfolio/
├── .env                          ← Variables de entorno (no versionado)
├── .gitignore
├── requirements.txt
├── manage.py
│
├── roberto_portfolio/            ← Configuración Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── cv_manager/                   ← App principal
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── templates/
│   ├── base.html
│   └── cv_manager/
│       ├── inicio.html
│       └── proyectos.html
│
├── static/
│   ├── css/custom.css
│   └── img/profile_photo.png
│
└── media/                        ← Archivos subidos (ImageField)
```

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/alke_web_cv.git
cd alke_web_cv
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
```

### 5. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a:

| URL | Descripción |
|---|---|
| `http://localhost:8000/` | CV completo (Home) |
| `http://localhost:8000/proyectos/` | Galería de proyectos |
| `http://localhost:8000/admin/` | Panel de administración |

---

## 💾 Modelos de Datos

| Modelo | Descripción | Cardinalidad |
|---|---|---|
| `Profile` | Datos personales, título profesional, bio y foto | Único |
| `Experience` | Empresa, cargo y fechas | Lista (ordenada por fecha) |
| `Achievement` | Logros vinculados a una experiencia (FK) | Lista (1:N con Experience) |
| `Education` | Título, institución y año de egreso | Lista |
| `Skill` | Nombre y categoría (`hard` / `soft`) | Lista |
| `Project` | Nombre, descripción, stack y flag `featured` | Lista |
| `Language` | Idioma y nivel (A1–C2 / Nativo) | Lista |

---

## 🌿 Convenciones Git

### Ramas

```
main          ← producción / entrega final
develop       ← integración continua
feature/*     ← una rama por Task
fix/*         ← correcciones de bugs
```

### Commits (Conventional Commits)

```
<tipo>(<scope>): <descripción imperativa>

feat(models): add Achievement model with FK to Experience
fix(admin): register Language model in admin site
style(templates): add Bootstrap badges for hard skills section
docs(readme): add installation and setup instructions
chore(deps): add python-decouple to requirements.txt
```

---

## 📄 Licencia

Este proyecto fue desarrollado como parte del Bootcamp Desarrollo de Aplicaciones Fullstack Python Trainee — Módulo #6 (Alke Solutions / ABP).
