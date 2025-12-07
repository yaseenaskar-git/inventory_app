@echo off
cd C:\Users\yasee\inventory_app
call venv\Scripts\activate.bat
python manage.py test test_receipt_integration -v 2
pause
