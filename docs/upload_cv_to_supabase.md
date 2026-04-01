# Script: `upload_cv_to_supabase.py`

Script Python para cargar los datos del CV desde `cv_roberto_otarola.json` a Supabase (PostgreSQL) usando la API REST de Supabase vía `supabase-py`.

---

## Requisitos

```bash
pip install supabase python-decouple
```

Crear `.env` en la raíz del proyecto:

```env
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...   # service_role key (nunca la anon key)
```

> ⚠️ **Usar la `service_role` key**, no la `anon` key. La `service_role` omite Row Level Security y permite escritura sin restricciones. Nunca exponerla en el frontend.

---

## Código

```python
#!/usr/bin/env python3
"""
upload_cv_to_supabase.py
────────────────────────
Carga cv_roberto_otarola.json en las tablas de Supabase
que corresponden a los modelos Django de alke_web_cv.

Uso:
    python upload_cv_to_supabase.py                   # carga completa
    python upload_cv_to_supabase.py --dry-run         # sin escritura
    python upload_cv_to_supabase.py --table profile   # solo una tabla

Variables de entorno requeridas (.env):
    SUPABASE_URL   → URL del proyecto Supabase
    SUPABASE_KEY   → service_role key
"""

import argparse
import json
import sys
from pathlib import Path

from decouple import config
from supabase import create_client, Client


# ── Configuración ─────────────────────────────────────────────────────────────

SUPABASE_URL: str = config('SUPABASE_URL')
SUPABASE_KEY: str = config('SUPABASE_KEY')
CV_JSON_PATH: Path = Path(__file__).parent / 'cv_roberto_otarola.json'

# Mapeo: clave JSON → nombre de tabla en Supabase
# Las tablas deben existir previamente (generadas por `python manage.py migrate`)
TABLE_MAP = {
    'profile':       'cv_profile',
    'skills':        'cv_skill',
    'experiences':   'cv_experience',
    'education':     'cv_education',
    'languages':     'cv_language',
    'certifications':'cv_certification',
    'publications':  'cv_publication',
    'presentations': 'cv_presentation',
    'projects':      'cv_project',
}


# ── Cliente Supabase ──────────────────────────────────────────────────────────

def get_client() -> Client:
    """Crea y devuelve el cliente Supabase."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ── Carga de datos ────────────────────────────────────────────────────────────

def clear_table(supabase: Client, table: str, dry_run: bool) -> None:
    """Borra todos los registros de una tabla antes de recargar."""
    if dry_run:
        print(f"  [DRY-RUN] DELETE FROM {table}")
        return
    # Supabase requiere un filtro; usamos neq en id para borrar todo
    supabase.table(table).delete().neq('id', 0).execute()
    print(f"  ✓ Tabla '{table}' limpiada.")


def insert_rows(supabase: Client, table: str, rows: list[dict], dry_run: bool) -> None:
    """Inserta filas en la tabla indicada."""
    if not rows:
        print(f"  ⚠  Sin datos para '{table}'. Omitido.")
        return
    if dry_run:
        print(f"  [DRY-RUN] INSERT {len(rows)} fila(s) en {table}")
        return
    response = supabase.table(table).insert(rows).execute()
    if hasattr(response, 'error') and response.error:
        raise RuntimeError(f"Error insertando en '{table}': {response.error}")
    print(f"  ✓ {len(rows)} fila(s) insertada(s) en '{table}'.")


# ── Transformadores por entidad ───────────────────────────────────────────────
# Adaptan los campos del JSON al esquema de las tablas Django/Supabase.

def transform_profile(data: dict) -> list[dict]:
    p = data['profile']
    return [{
        'full_name':    p['full_name'],
        'title':        p['title'],
        'bio':          p['bio'],
        'location':     p['location'],
        'linkedin_url': p.get('linkedin_url', ''),
        'github_url':   p.get('github_url', ''),
        'photo':        '',  # se sube por separado desde el admin
    }]


def transform_skills(data: dict) -> list[dict]:
    return [
        {'name': s['name'], 'category': s['category']}
        for s in data['skills']
    ]


def transform_experiences(data: dict) -> tuple[list[dict], list[dict]]:
    """Devuelve (experiences, achievements) para inserción en 2 tablas."""
    experiences = []
    achievements = []
    for exp in data['experiences']:
        experiences.append({
            'company':    exp['company'],
            'role':       exp['role'],
            'location':   exp.get('location', ''),
            'start_date': exp['start_date'],
            'end_date':   exp.get('end_date'),   # None → NULL
        })
    # achievements se cargan en un segundo paso (requieren el id de experience)
    return experiences, data['experiences']


def transform_education(data: dict) -> list[dict]:
    return [
        {
            'degree':      e['degree'],
            'institution': e['institution'],
            'year':        e['end_year'],   # campo legacy del modelo actual
        }
        for e in data['education']
    ]


def transform_languages(data: dict) -> list[dict]:
    return [
        {'name': l['name'], 'level': l['level']}
        for l in data['languages']
    ]


def transform_projects(data: dict) -> list[dict]:
    return [
        {
            'name':        p['name'],
            'description': p['description'],
            'stack':       p.get('stack', ''),
            'repo_url':    p.get('repo_url', ''),
            'featured':    p.get('featured', False),
        }
        for p in data['projects']
    ]


def transform_certifications(data: dict) -> list[dict]:
    return [
        {
            'year':        c['year'],
            'name':        c['name'],
            'institution': c['institution'],
        }
        for c in data['certifications']
    ]


def transform_publications(data: dict) -> list[dict]:
    return [
        {
            'type_':       p['type'],
            'title':       p['title'],
            'event':       p['event'],
            'year':        p['year'],
            'role':        p['role'],
        }
        for p in data['publications']
    ]


def transform_presentations(data: dict) -> list[dict]:
    return [
        {
            'event':    p['event'],
            'location': p['location'],
            'year':     p['year'],
            'topic':    p['topic'],
        }
        for p in data['presentations']
    ]


# ── Carga de achievements (requiere IDs de Experience) ────────────────────────

def upload_achievements(supabase: Client, exp_source: list[dict], dry_run: bool) -> None:
    """
    Obtiene los IDs de Experience recién insertados y carga los Achievement.
    Supabase devuelve las filas insertadas con sus IDs autogenerados.
    """
    table_exp = TABLE_MAP['experiences']
    table_ach = 'cv_achievement'

    print(f"\n── Cargando achievements ──")
    clear_table(supabase, table_ach, dry_run)

    if dry_run:
        total = sum(len(e.get('achievements', [])) for e in exp_source)
        print(f"  [DRY-RUN] INSERT {total} achievement(s) en {table_ach}")
        return

    # Recuperar los IDs de las experiencias por company+role+start_date
    achievements_to_insert = []
    for exp in exp_source:
        result = (
            supabase.table(table_exp)
            .select('id')
            .eq('company', exp['company'])
            .eq('role', exp['role'])
            .eq('start_date', exp['start_date'])
            .limit(1)
            .execute()
        )
        if not result.data:
            print(f"  ⚠  No se encontró Experience para '{exp['role']} @ {exp['company']}'. Achievements omitidos.")
            continue
        exp_id = result.data[0]['id']
        for desc in exp.get('achievements', []):
            achievements_to_insert.append({
                'experience_id': exp_id,
                'description':   desc,
            })

    if achievements_to_insert:
        response = supabase.table(table_ach).insert(achievements_to_insert).execute()
        if hasattr(response, 'error') and response.error:
            raise RuntimeError(f"Error insertando achievements: {response.error}")
        print(f"  ✓ {len(achievements_to_insert)} achievement(s) insertado(s).")


# ── Orquestador principal ─────────────────────────────────────────────────────

def upload_all(data: dict, supabase: Client, only: str | None, dry_run: bool) -> None:
    """Ejecuta la carga completa o de una tabla específica."""

    tasks = {
        'profile':        (TABLE_MAP['profile'],        transform_profile(data)),
        'skills':         (TABLE_MAP['skills'],          transform_skills(data)),
        'education':      (TABLE_MAP['education'],       transform_education(data)),
        'languages':      (TABLE_MAP['languages'],       transform_languages(data)),
        'certifications': (TABLE_MAP['certifications'],  transform_certifications(data)),
        'publications':   (TABLE_MAP['publications'],    transform_publications(data)),
        'presentations':  (TABLE_MAP['presentations'],   transform_presentations(data)),
        'projects':       (TABLE_MAP['projects'],        transform_projects(data)),
    }

    for key, (table, rows) in tasks.items():
        if only and key != only:
            continue
        print(f"\n── {key.upper()} → {table} ──")
        clear_table(supabase, table, dry_run)
        insert_rows(supabase, table, rows, dry_run)

    # Experiences + Achievements (2 tablas relacionadas)
    if not only or only == 'experiences':
        experiences, exp_source = transform_experiences(data)
        print(f"\n── EXPERIENCES → {TABLE_MAP['experiences']} ──")
        clear_table(supabase, TABLE_MAP['experiences'], dry_run)
        insert_rows(supabase, TABLE_MAP['experiences'], experiences, dry_run)
        upload_achievements(supabase, exp_source, dry_run)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Carga cv_roberto_otarola.json en Supabase.'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Muestra qué se haría sin escribir nada.'
    )
    parser.add_argument(
        '--table', metavar='NAME',
        choices=list(TABLE_MAP.keys()),
        help='Carga solo la tabla indicada (ej: profile, skills, experiences).'
    )
    args = parser.parse_args()

    # Leer JSON
    if not CV_JSON_PATH.exists():
        print(f"❌ No se encontró '{CV_JSON_PATH}'. Verifica la ruta.", file=sys.stderr)
        sys.exit(1)

    with CV_JSON_PATH.open(encoding='utf-8') as f:
        data = json.load(f)

    print(f"{'[DRY-RUN] ' if args.dry_run else ''}Conectando a Supabase: {SUPABASE_URL}")
    supabase = get_client()

    print(f"\n🚀 Iniciando carga del CV en Supabase...")
    upload_all(data, supabase, only=args.table, dry_run=args.dry_run)
    print(f"\n✅ Carga completada {'(dry-run)' if args.dry_run else ''}.")


if __name__ == '__main__':
    main()
```

---

## Uso

```bash
# Verificar sin escribir
python upload_cv_to_supabase.py --dry-run

# Cargar todo
python upload_cv_to_supabase.py

# Cargar solo una tabla
python upload_cv_to_supabase.py --table profile
python upload_cv_to_supabase.py --table skills
python upload_cv_to_supabase.py --table experiences
```

---

## Flujo completo de deploy

```
1. python manage.py migrate          # crea las tablas en Supabase
2. python upload_cv_to_supabase.py --dry-run   # verifica sin escribir
3. python upload_cv_to_supabase.py             # carga los datos
4. git push → Render redeploya automáticamente
```

---

## Notas importantes

| Tema | Detalle |
|------|---------|
| **Clave usada** | `service_role` key (no `anon` key) — omite Row Level Security |
| **Idempotente** | Sí: borra y recarga en cada ejecución (seguro para CI) |
| **Tabla `cv_achievement`** | Requiere que `cv_experience` esté cargada primero |
| **Campo `photo` en `cv_profile`** | Se sube manualmente desde el admin de Django |
| **`.env` en `.gitignore`** | Verificar que `.env` esté excluido del repositorio |
| **Supabase session pooler** | Para Render, usar la connection string del **Transaction pooler** (puerto 6543), no la directa |
