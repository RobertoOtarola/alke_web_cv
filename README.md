# 🐍 CV Dinámico & Portafolio Técnico

**Bootcamp Desarrollo de Aplicaciones Fullstack Python Trainee | Módulo #7 | Reingeniería & Deploy**

Esta aplicación ha sido reestructurada como una plataforma profesional que separa la presentación del currículum dinámico (`cv`) de la galería de proyectos técnicos (`portfolio`). Utiliza una arquitectura moderna orientada al dominio, estilizada con el kit de marca **Earthy & Trustworthy** (Deep Teal, Warm Gold, Vibrant Green).

---

## 📋 Tabla de Contenidos

- [✨ Características](#-características)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [🚀 Instalación y Uso Local](#-instalación-y-uso-local)
- [☁️ Sincronización con Supabase](#-sincronización-con-supabase)
- [🌐 Despliegue a Producción](#-despliegue-a-producción-render--supabase)

---

## ✨ Características

- **Dos Aplicaciones Nucleares:**
  - `cv`: Gestión del perfil profesional, habilidades, experiencia laboral, educación y certificaciones.
  - `portfolio`: Hub de empleabilidad con galería de proyectos y **Casos de Estudio** dinámicos.
- **Frontend Premium:** Rediseño completo usando **Bootstrap 5.3** y **jQuery**.
  - **Scroll Reveal & Animations**: Efectos visuales fluidos al navegar.
  - **Dark Mode**: Toggle inteligente para comodidad visual.
  - **Project Search & Filters**: Búsqueda en tiempo real de proyectos y filtrado por tecnologías.
  - **Skill Badges & Counters**: Visualización dinámica de estadísticas y habilidades.
  - **Glassmorphism Hero**: Diseño moderno con efectos de transparencia.
- **Sincronización Automática**: Script para poblar la base de datos remota de Supabase desde un archivo JSON estructurado.

---

## 🛠 Tech Stack

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| Django 6.0 | Framework web |
| jQuery | Lógica de interactividad frontend |
| Bootstrap 5.3 | Sistema de diseño y layout |
| Supabase (Postgres) | Base de Datos en producción |
| WhiteNoise | Gestión de archivos estáticos |
| Python-Decouple | Gestión de variables de entorno segura |

---

## 📁 Estructura del Proyecto

```text
alke_web_cv/
├── apps/
│   ├── cv/                 ← CV Dinámico (Modelos: Profile, Experience, Skill, etc.)
│   └── portfolio/          ← Proyectos y Casos de Estudio (Slug-driven detail views)
├── config/                 ← Configuración centralizada (Settings local/production)
├── templates/
│   ├── base.html           ← Layout con Navbar y Footer unificados
│   ├── cv/                 ← index.html (CV Personal)
│   └── portfolio/          ← landing.html (Showcase) y projects.html (Lista completa)
├── static/
│   ├── css/custom.css      ← Design System (Earthy & Trustworthy tokens)
│   ├── js/main.js          ← Lógica jQuery (Filtros, Dark mode, Animaciones)
│   └── img/portfolio/      ← Assets de proyectos
├── upload_cv_to_supabase.py ← Herramienta de sincronización JSON → DB
└── cv_roberto_otarola.json  ← Fuente de veracidad de datos del CV
```

---

## 🚀 Instalación y Uso Local

1. **Clonar e instalar dependencias:**
   ```bash
   git clone https://github.com/robertootarola/alke_web_cv.git
   cd alke_web_cv
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configurar el entorno (`.env`):**
   Crea un archivo `.env` basado en los requerimientos del proyecto:
   ```env
   SECRET_KEY=tu_secreto
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   # Para usar el script de carga:
   SUPABASE_URL=tu_url_supabase
   SUPABASE_KEY=tu_service_role_key
   ```

3. **Migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## ☁️ Sincronización con Supabase

Para cargar de forma masiva los datos de tu CV y asegurar que la base de datos remota esté sincronizada con `cv_roberto_otarola.json`, utiliza el script automatizado:

```bash
# Sincronización total (Carga de las 10 entidades)
python upload_cv_to_supabase.py

# Verificación sin escribir cambios
python upload_cv_to_supabase.py --dry-run
```

Este script limpia las tablas existentes y reinserta los datos manteniendo la integridad referencial (Achievements v/s Experiences).

---

## 🌐 Despliegue a Producción (Render)

1. En Render, crea un **Web Service**.
2. **Build Command**: `bash build.sh`
3. **Start Command**: `gunicorn config.wsgi:application`
4. Define las variables de entorno, incluyendo `DJANGO_SETTINGS_MODULE=config.settings.production`.

---

## 📄 Licencia
GPL-3.0
