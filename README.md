# 🐍 CV Dinámico

**Bootcamp Desarrollo de Aplicaciones Fullstack Python Trainee | Módulo #7 | Deploy**

Aplicación web Django profesional para editar y renderizar un Curriculum Vitae dinámico. Esta versión incluye refactorización de arquitectura orientada al dominio (`apps/cv`), separación estricta de entornos de configuración y todo lo necesario para despliegue en producción usando **Render** (servidor web) y **Supabase** (PostgreSQL).

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tech Stack](#-tech-stack)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación y Uso Local](#-instalación-y-uso-local)
- [Población Dinámica del CV](#-población-dinámica-del-cv)
- [Despliegue a Producción](#-despliegue-a-producción-render--supabase)
- [Convenciones Git](#-convenciones-git)

---

## ✨ Características

- **Arquitectura de Dominio** — Separación del core (`config`) de la lógica de negocio (`apps/cv`).
- **Configuración Enrutada** — División limpia entre entornos locales (`local.py`) y de producción (`production.py`).
- **Despliegue Continuo (CI/CD Ready)** — Funciona nativamente en Render mediante `build.sh`.
- **CV Administrable** — Panel avanzado en Django Admin con `AchievementInline`.
- **Seguridad** — Envvars aisladas con `python-decouple`, control HTTPS directo y Cookies Seguras implementadas para producción.

---

## 🛠 Tech Stack

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje principal |
| Django 6.0 | Framework web |
| Gunicorn & WhiteNoise| Servidor backend de producción y renderizado de recursos estáticos |
| Supabase (PostgreSQL)| Base de Datos en la nube (producción) |
| SQLite | Base de datos por defecto (desarrollo local) |

---

## 📁 Estructura del Proyecto

```text
alke_web_cv/
├── .env                          ← Variables de entorno (ignorado en git)
├── requirements.txt              ← Dependencias de producción
├── build.sh                      ← Script de construcción automático para Render
├── populate_cv.py                ← Script de semilla (Seed) de la Base de Datos
├── manage.py
│
├── config/                       ← Configuración centralizada
│   ├── settings/
│   │   ├── base.py               ← Lógica general compartida 
│   │   ├── local.py              ← Solo desarrollo y SQLite
│   │   └── production.py         ← Reglas de seguridad + PostgreSQL para Render
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/                         ← Módulos de aplicación
│   └── cv/                       ← Lógica del CV dinámico
│       ├── models.py
│       ├── views.py
│       └── ...
│
├── templates/
│   ├── base.html
│   └── cv/                       ← Vistas HTML del CV
│
├── static/                       ← Archivos de diseño CSS e imágenes
└── media/                        ← Imágenes de perfil e integraciones multimedias cargadas
```

---

## 🚀 Instalación y Uso Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/robertootarola/alke_web_cv.git
cd alke_web_cv
```

### 2. Entorno virtual & Dependencias
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# o venv\Scripts\activate para Windows

pip install -r requirements.txt
```

### 3. Configurar variables de entorno (`.env`)
Crear un archivo `.env` en la raíz del proyecto para ambiente de desarrollo:
```env
SECRET_KEY=tu-clave-secreta-de-desarrollo
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 4. Migraciones
El proyecto automáticamente cargará el entorno `local.py`:
```bash
python manage.py makemigrations cv
python manage.py migrate
```

---

## 🌱 Población Dinámica del CV

Este proyecto cuenta con un script capaz de cargar todos los datos base del CV a la Base de Datos en un solo paso ahorrando ingresos manuales.
Tras terminar las migraciones, corre este comando por consola:

```bash
python populate_cv.py
```
*Inyectará automáticamente todo tu perfil profesional, experiencias (como AUTOENERGIAS), estudios y habilidades. Luego podrás editarlas libremente en http://localhost:8000/admin.*

Puedes abrir el servidor localmente con `python manage.py runserver` y visualizar tus logros. 

---

## 🌐 Despliegue a Producción (Render + Supabase)

### Paso 1: Base de Datos (Supabase)
Crea un proyecto gratuito en **Supabase**, dirígete a Database Settings y extrae tu `DATABASE_URL`. Reemplaza tu contraseña (evita caracteres especiales extraños para no corromper la URI).

### Paso 2: Servidor (Render)
1. Conecta tu cuenta de Github a **Render** y crea un nuevo *Web Service*.
2. **Build Command**: `bash build.sh`
3. **Start Command**: `gunicorn config.wsgi:application`
4. Carga las variables de entorno (*Environment Variables*):
   - `DATABASE_URL`: Pegar tu URL de Supabase PostgreSQL.
   - `SECRET_KEY`: Una clave alfanumérica encriptada.
   - `DJANGO_SETTINGS_MODULE`: `config.settings.production`
   - `ALLOWED_HOSTS`: `alke-cv-web.onrender.com`

---

## 🌿 Convenciones Git

**Ramas:**
- `main`: Producción / despliegue en Render (Release versions).
- `develop`: Integración continua de funcionalidades.
- `feature/*`: Desarrollo de nuevas capacidades aisladas del CV.

---

## 📄 Licencia

GPL-3.0
