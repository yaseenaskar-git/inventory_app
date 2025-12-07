#!/bin/bash
# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear 2>/dev/null || true

# Start Django with gunicorn on the PORT environment variable (default 8080 for Cloud Run)
echo "Starting Django server with gunicorn on port ${PORT:-8080}..."
gunicorn inventory_app.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 4 --threads 2 --worker-class gthread --timeout 120
