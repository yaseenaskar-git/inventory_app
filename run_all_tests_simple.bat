@echo off
cd C:\Users\yasee\inventory_app
call venv\Scripts\activate.bat
python manage.py test accounts test_receipt_integration
pause
