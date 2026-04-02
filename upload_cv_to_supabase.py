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

from decouple import config          # pylint: disable=import-error
from supabase import create_client, Client  # pylint: disable=import-error


# ── Configuración ─────────────────────────────────────────────────────────────

SUPABASE_URL: str = config('SUPABASE_URL')
SUPABASE_KEY: str = config('SUPABASE_KEY')
CV_JSON_PATH: Path = Path(__file__).parent / 'cv_roberto_otarola.json'

# Mapeo: clave JSON → nombre de tabla en Supabase
# Las tablas deben existir previamente (generadas por `python manage.py migrate`)
TABLE_MAP = {
    'profile':        'cv_profile',
    'skills':         'cv_skill',
    'experiences':    'cv_experience',
    'education':      'cv_education',
    'languages':      'cv_language',
    'certifications': 'cv_certification',
    'publications':   'cv_publication',
    'presentations':  'cv_presentation',
    'projects':       'portfolio_proyecto',
}


# ── Cliente Supabase ──────────────────────────────────────────────────────────

def get_client() -> Client:
    """Crea y devuelve el cliente Supabase autenticado con la service_role key."""
    return create_client(SUPABASE_URL, SUPABASE_KEY)


# ── Carga de datos ────────────────────────────────────────────────────────────

def clear_table(supabase: Client, table: str, dry_run: bool) -> None:
    """Borra todos los registros de una tabla antes de recargar."""
    if dry_run:
        print(f"  [DRY-RUN] DELETE FROM {table}")
        return
    supabase.table(table).delete().neq('id', 0).execute()
    print(f"  ✓ Tabla '{table}' limpiada.")


def insert_rows(supabase: Client, table: str, rows: list, dry_run: bool) -> None:
    """Inserta una lista de filas en la tabla indicada de Supabase."""
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

def transform_profile(data: dict) -> list:
    """Transforma el bloque 'profile' del JSON al formato de la tabla cv_profile."""
    p = data['profile']
    return [{
        'full_name':    p['full_name'],
        'title':        p['title'],
        'bio':          p['bio'],
        'location':     p['location'],
        'linkedin_url': p.get('linkedin_url', ''),
        'github_url':   p.get('github_url', ''),
        'photo':        '',
    }]


def transform_skills(data: dict) -> list:
    """Transforma el bloque 'skills' del JSON al formato de la tabla cv_skill."""
    return [
        {'name': s['name'], 'category': s['category']}
        for s in data['skills']
    ]


def transform_experiences(data: dict) -> tuple:
    """
    Transforma el bloque 'experiences' del JSON.

    Devuelve una tupla (experiences, raw_source) donde:
    - experiences: filas listas para insertar en cv_experience.
    - raw_source: lista original con los achievements para un segundo paso.
    """
    experiences = [
        {
            'company':    exp['company'],
            'role':       exp['role'],
            'location':   exp.get('location', ''),
            'start_date': exp['start_date'],
            'end_date':   exp.get('end_date'),
        }
        for exp in data['experiences']
    ]
    return experiences, data['experiences']


def transform_education(data: dict) -> list:
    """Transforma el bloque 'education' del JSON al formato de la tabla cv_education."""
    return [
        {
            'degree':      e['degree'],
            'institution': e['institution'],
            'year':        e['end_year'],
        }
        for e in data['education']
    ]


def transform_languages(data: dict) -> list:
    """Transforma el bloque 'languages' del JSON al formato de la tabla cv_language."""
    return [
        {'name': lang['name'], 'level': lang['level']}
        for lang in data['languages']
    ]


def transform_projects(data: dict) -> list:
    """Transforma el bloque 'projects' del JSON al formato de la tabla portfolio_proyecto."""
    return [
        {
            'nombre':          p['name'],
            'descripcion':     p['description'],
            'tecnologias':     p.get('stack', ''),
            'url_repositorio': p.get('repo_url', ''),
            'destacado':       p.get('featured', False),
            # 'url_demo' e 'imagen_url' se manejarán vía fixture o edición manual
        }
        for p in data['projects']
    ]


def transform_certifications(data: dict) -> list:
    """Transforma el bloque 'certifications' del JSON al formato de cv_certification."""
    return [
        {
            'year':        c['year'],
            'name':        c['name'],
            'institution': c['institution'],
        }
        for c in data['certifications']
    ]


def transform_publications(data: dict) -> list:
    """Transforma el bloque 'publications' del JSON al formato de cv_publication."""
    return [
        {
            'publication_type':  p['type'],
            'title':  p['title'],
            'event':  p['event'],
            'year':   p['year'],
            'role':   p['role'],
        }
        for p in data['publications']
    ]


def transform_presentations(data: dict) -> list:
    """Transforma el bloque 'presentations' del JSON al formato de cv_presentation."""
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

def upload_achievements(supabase: Client, exp_source: list, dry_run: bool) -> None:
    """
    Carga los Achievement vinculados a cada Experience.

    Recupera el ID autogenerado de cada Experience recién insertada
    filtrando por (company, role, start_date) y luego inserta los
    achievements en cv_achievement con la FK correcta.
    """
    table_exp = TABLE_MAP['experiences']
    table_ach = 'cv_achievement'

    print("\n── Cargando achievements ──")
    clear_table(supabase, table_ach, dry_run)

    if dry_run:
        total = sum(len(e.get('achievements', [])) for e in exp_source)
        print(f"  [DRY-RUN] INSERT {total} achievement(s) en {table_ach}")
        return

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
            print(
                f"  ⚠  No se encontró Experience para "
                f"'{exp['role']} @ {exp['company']}'. Achievements omitidos."
            )
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

def upload_all(data: dict, supabase: Client, only: str, dry_run: bool) -> None:
    """
    Ejecuta la carga completa o de una entidad específica.

    Args:
        data:     Contenido completo del JSON del CV.
        supabase: Cliente Supabase autenticado.
        only:     Si se especifica, carga solo esa entidad; None = todas.
        dry_run:  Si True, no escribe nada en la base de datos.
    """
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

    if not only or only == 'experiences':
        experiences, exp_source = transform_experiences(data)
        print(f"\n── EXPERIENCES → {TABLE_MAP['experiences']} ──")
        clear_table(supabase, TABLE_MAP['experiences'], dry_run)
        insert_rows(supabase, TABLE_MAP['experiences'], experiences, dry_run)
        upload_achievements(supabase, exp_source, dry_run)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    """Punto de entrada principal. Parsea argumentos y lanza la carga."""
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

    if not CV_JSON_PATH.exists():
        print(f"❌ No se encontró '{CV_JSON_PATH}'. Verifica la ruta.", file=sys.stderr)
        sys.exit(1)

    with CV_JSON_PATH.open(encoding='utf-8') as f:
        data = json.load(f)

    prefix = "[DRY-RUN] " if args.dry_run else ""
    print(f"{prefix}Conectando a Supabase: {SUPABASE_URL}")
    supabase = get_client()

    print("\n🚀 Iniciando carga del CV en Supabase...")
    upload_all(data, supabase, only=args.table, dry_run=args.dry_run)

    suffix = "(dry-run)" if args.dry_run else ""
    print(f"\n✅ Carga completada {suffix}.")


if __name__ == '__main__':
    main()
