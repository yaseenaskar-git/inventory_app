#!/bin/bash
# Start Django on the PORT environment variable (default 8080 for Cloud Run)
python manage.py runserver 0.0.0.0:${PORT:-8080}
