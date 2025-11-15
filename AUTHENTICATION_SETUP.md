# Authentication Feature Setup Guide

## Overview
This guide walks you through setting up and running the authentication feature for the Inventory Management System.

## Prerequisites
- Python 3.8+
- Django 5.2.8
- pip (Python package manager)

## Setup Steps

### 1. Create Virtual Environment (if not already done)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Required Packages
```bash
pip install django==5.2.8
```

### 3. Run Migrations
```bash
python manage.py migrate
```

This will create the necessary database tables for user authentication.

### 4. Create a Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. You can use this to access `/admin/`.

### 5. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

## Usage

### User Registration
1. Navigate to `http://localhost:8000/accounts/register/`
2. Enter email and password (password must be at least 8 characters)
3. Passwords must match
4. Email must be unique
5. After successful registration, you'll be automatically logged in and redirected to the dashboard

### User Login
1. Navigate to `http://localhost:8000/accounts/login/`
2. Enter your email and password
3. Click "Login"
4. On success, you'll be redirected to the dashboard

### Dashboard
- Only accessible to authenticated users
- Shows a welcome message with your email
- Contains a logout button
- Placeholder for future features (inventories, analytics)

### Logout
1. Click the "Logout" button on the dashboard
2. You'll be redirected to the login page

## Features Implemented

✅ **User Registration**
- Email-based registration
- Password strength validation
- Duplicate email prevention
- Automatic login after registration

✅ **User Login**
- Email and password authentication
- Error handling for invalid credentials
- Session management

✅ **User Logout**
- Secure session termination
- Redirect to login page

✅ **Authentication Protection**
- Dashboard requires login
- Automatic redirect to login for unauthenticated users
- Django's built-in `@login_required` decorator

✅ **Password Security**
- Bcrypt hashing (Django default)
- Password validation rules
- Password confirmation on registration

✅ **User Interface**
- Bootstrap 5 styling
- Responsive design
- Flash messages for user feedback
- Error display on forms

## File Structure

```
accounts/
├── migrations/           # Database migrations
├── templates/accounts/
│   ├── base.html        # Base template with styling
│   ├── register.html    # Registration form
│   ├── login.html       # Login form
│   └── dashboard.html   # User dashboard
├── __init__.py
├── admin.py            # Admin configuration
├── apps.py             # App configuration
├── forms.py            # Registration and login forms
├── models.py           # Database models
├── tests.py            # Unit tests
├── urls.py             # URL routes
└── views.py            # View functions
```

## Testing

Run the test suite:
```bash
python manage.py test accounts
```

Tests include:
- User registration success and validation
- User login success and validation
- Dashboard access control
- Logout functionality
- Duplicate email prevention
- Password mismatch handling

## Security Notes

1. **Password Hashing**: Uses Django's default PBKDF2 algorithm
2. **CSRF Protection**: All forms include CSRF tokens
3. **Session Management**: Django's built-in session framework
4. **Login Required**: Dashboard protected with `@login_required` decorator

## Future Enhancements

- Email verification
- Password reset functionality
- Social authentication (Google, GitHub)
- Two-factor authentication
- User profile customization
- Account deletion

## Troubleshooting

### Issues with migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Database reset (development only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port already in use
```bash
python manage.py runserver 8001
```
