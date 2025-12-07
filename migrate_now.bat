@echo off
cd C:\Users\yasee\inventory_app
call venv\Scripts\activate.bat
python manage.py migrate accounts
pause
