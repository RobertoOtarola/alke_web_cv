#!/usr/bin/env bash
# build.sh — Script de construcción para Render

set -o errexit    # Detener si hay un error

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
# NOTA: cv:0006 da error en Supabase porque los campos ya existen. Se marca como falsa.
python manage.py migrate cv 0006 --fake --no-input

# Aplicar el resto de las migraciones
python manage.py migrate --no-input
