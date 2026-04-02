from django.db import migrations

def apply_resilient_schema(apps, schema_editor):
    """
    Aplica las operaciones de esquema de forma resiliente para corregir desincronización
    entre el historial de migraciones y la base de datos real (Supabase).
    Soporta PostgreSQL y SQLite.
    """
    connection = schema_editor.connection
    vendor = connection.vendor

    if vendor == 'postgresql':
        # 1. Asegurar borrado de tabla Project redundante si existe
        schema_editor.execute('DROP TABLE IF EXISTS "cv_project";')

        # 2. Agregar columnas faltantes con IF NOT EXISTS
        schema_editor.execute('ALTER TABLE "cv_education" ADD COLUMN IF NOT EXISTS "start_year" smallint NULL;')
        schema_editor.execute('ALTER TABLE "cv_experience" ADD COLUMN IF NOT EXISTS "featured" boolean NOT NULL DEFAULT FALSE;')
        schema_editor.execute('ALTER TABLE "cv_experience" ADD COLUMN IF NOT EXISTS "location" varchar(100) NOT NULL DEFAULT \'\';')
        schema_editor.execute('ALTER TABLE "cv_profile" ADD COLUMN IF NOT EXISTS "email" varchar(254) NOT NULL DEFAULT \'\';')

    elif vendor == 'sqlite':
        # En SQLite local, probablemente ya existen por el historial estándar, 
        # pero implementamos chequeos para evitar errores en tests.
        def add_col_sqlite(table, column, definition):
            cursor = connection.cursor()
            cursor.execute(f"PRAGMA table_info({table});")
            existing_cols = [row[1] for row in cursor.fetchall()]
            if column not in existing_cols:
                schema_editor.execute(f'ALTER TABLE {table} ADD COLUMN {column} {definition};')

        add_col_sqlite("cv_education", "start_year", "smallint NULL")
        add_col_sqlite("cv_experience", "featured", "bool NOT NULL DEFAULT 0")
        add_col_sqlite("cv_experience", "location", "varchar(100) NOT NULL DEFAULT ''")
        add_col_sqlite("cv_profile", "email", "varchar(254) NOT NULL DEFAULT ''")

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('cv', '0007_delete_project'),
    ]

    operations = [
        migrations.RunPython(apply_resilient_schema, reverse_code=noop),
    ]
