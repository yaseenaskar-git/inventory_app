#!/bin/bash
# Quick setup script for macOS/Linux

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Running migrations..."
python manage.py migrate

echo ""
echo "Creating superuser (admin account)..."
python manage.py createsuperuser

echo ""
echo "Setup complete! Starting development server..."
python manage.py runserver
