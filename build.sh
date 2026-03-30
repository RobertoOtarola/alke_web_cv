#!/usr/bin/env bash
# build.sh — Script de construcción para Render

set -o errexit    # Detener si hay un error

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos
python manage.py collectstatic --no-input

# Aplicar migraciones
python manage.py migrate
