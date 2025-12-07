@echo off
cd C:\Users\yasee\inventory_app
call venv\Scripts\activate.bat
python manage.py test accounts.tests.test_backend accounts.tests.test_frontend test_receipt_integration
pause
