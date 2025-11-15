# Accounts App - User Authentication

This directory contains the user authentication system for the Inventory Management Application.

## 📁 Structure

```
accounts/
├── migrations/              # Database migration files
├── templates/accounts/      # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   ├── register.html       # Registration form
│   ├── login.html          # Login form
│   └── dashboard.html      # User dashboard
├── __init__.py             # Package initialization
├── admin.py                # Django admin configuration
├── apps.py                 # App configuration
├── forms.py                # Registration & login forms
├── models.py               # Database models
├── tests.py                # Unit tests
├── urls.py                 # URL routing
├── utils.py                # Utility functions
└── views.py                # View functions
```

## 🔐 Features

- **User Registration**: Create accounts with email and password
- **User Login**: Authenticate with credentials
- **User Logout**: Secure session termination
- **Protected Dashboard**: Access control for authenticated users
- **Form Validation**: Email uniqueness and password strength
- **Error Handling**: User-friendly error messages
- **CSRF Protection**: Token-based protection
- **Responsive UI**: Bootstrap 5 styling

## 📝 Key Files

### forms.py
- `RegisterForm`: User registration form with validation
- `LoginForm`: User login form

### views.py
- `register()`: Handle user registration
- `login_view()`: Handle user login
- `logout_view()`: Handle user logout
- `dashboard()`: Protected user dashboard

### urls.py
Routes:
- `accounts/register/` → Register
- `accounts/login/` → Login
- `accounts/logout/` → Logout (protected)
- `accounts/dashboard/` → Dashboard (protected)

### models.py
Uses Django's built-in `User` model:
- Email-based authentication
- Password hashing (PBKDF2)
- Session management

### tests.py
10 comprehensive unit tests:
- Registration success/validation
- Login success/validation
- Access control
- Logout functionality
- Error handling

## 🚀 Quick Start

### Initialize
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Run Tests
```bash
python manage.py test accounts
```

### Access
- Registration: http://localhost:8000/accounts/register/
- Login: http://localhost:8000/accounts/login/
- Dashboard: http://localhost:8000/accounts/dashboard/
- Admin: http://localhost:8000/admin/

## 🔒 Security Features

- ✅ Password hashing (PBKDF2 with SHA256)
- ✅ Email validation and uniqueness check
- ✅ Password confirmation on registration
- ✅ CSRF token protection
- ✅ Session-based authentication
- ✅ `@login_required` decorators
- ✅ Input validation
- ✅ Generic error messages (no info leakage)

## 📚 Documentation

See the main documentation files:
- [QUICK_START_GUIDE.md](../QUICK_START_GUIDE.md)
- [PROJECT_DOCUMENTATION.md](../PROJECT_DOCUMENTATION.md)
- [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)

## 🧪 Testing

All features are tested:
```bash
python manage.py test accounts -v 2
```

## 🎯 Future Enhancements

- [ ] Email verification
- [ ] Password reset
- [ ] Social authentication
- [ ] Two-factor authentication
- [ ] User profiles
- [ ] Account deletion
- [ ] Activity logging

---

**Status**: ✅ Production Ready (after configuration)
