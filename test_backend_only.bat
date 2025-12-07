@echo off
cd C:\Users\yasee\inventory_app
call venv\Scripts\activate.bat
python manage.py test accounts.tests.test_backend -v 2
pause
