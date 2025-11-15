# Inventory Management System - Authentication Feature

## 🎯 Project Overview

This is a Django-based inventory management system with a focus on secure user authentication. Users can create accounts, log in securely, and access their personalized dashboard.

## ✨ Features Implemented

### Authentication System
- ✅ User Registration with email validation
- ✅ Secure Password Hashing (PBKDF2)
- ✅ User Login with session management
- ✅ User Logout functionality
- ✅ Dashboard access control
- ✅ CSRF protection on all forms
- ✅ Flash messages for user feedback
- ✅ Responsive Bootstrap UI

### Security Features
- ✅ Password strength validation (min 8 characters)
- ✅ Password confirmation on registration
- ✅ Duplicate email prevention
- ✅ Django's built-in authentication system
- ✅ Session-based authentication
- ✅ Login required decorators

## 📁 Project Structure

```
inventory_app/
├── accounts/                    # Authentication app
│   ├── migrations/             # Database migrations
│   ├── templates/accounts/     # HTML templates
│   │   ├── base.html          # Base template with Bootstrap
│   │   ├── register.html      # Registration page
│   │   ├── login.html         # Login page
│   │   └── dashboard.html     # User dashboard
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Registration & login forms
│   ├── models.py             # Database models (using default User)
│   ├── tests.py              # Unit tests
│   ├── urls.py               # URL routing
│   ├── utils.py              # Helper utilities
│   └── views.py              # View functions
├── inventory_app/             # Project settings
│   ├── settings.py           # Django settings (MODIFIED)
│   ├── urls.py               # Main URL routing (MODIFIED)
│   ├── wsgi.py
│   └── asgi.py
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── AUTHENTICATION_SETUP.md   # Setup guide
├── PROJECT_DOCUMENTATION.md  # This file
├── setup.bat                 # Windows setup script
├── setup.sh                  # macOS/Linux setup script
└── README.md
```

## 🚀 Quick Start

### Option 1: Using Setup Script

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
bash setup.sh
```

### Option 2: Manual Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Frontend: http://localhost:8000/
   - Admin: http://localhost:8000/admin/

## 📝 URL Routes

```
/                           → Redirect to login
/accounts/register/         → User registration
/accounts/login/            → User login
/accounts/logout/           → User logout (requires authentication)
/accounts/dashboard/        → User dashboard (requires authentication)
/admin/                     → Django admin panel (superuser only)
```

## 🔐 User Workflows

### Registration Flow
1. User visits `/accounts/register/`
2. Fills in email and password (twice for confirmation)
3. Form validates:
   - Email must be unique
   - Password must be at least 8 characters
   - Passwords must match
4. On success:
   - User is created in database
   - User is automatically logged in
   - Redirected to dashboard
5. On error:
   - Form shows specific error messages
   - User remains on registration page

### Login Flow
1. User visits `/accounts/login/`
2. Enters email and password
3. System checks credentials:
   - Email exists in database
   - Password is correct
4. On success:
   - Session is created
   - User is redirected to dashboard
5. On error:
   - Generic error message (for security)
   - User remains on login page

### Dashboard Access
- Only accessible to authenticated users
- Redirect to login if not authenticated
- Shows personalized welcome message
- Contains logout button

## 🧪 Testing

### Run All Tests
```bash
python manage.py test accounts
```

### Run Specific Test
```bash
python manage.py test accounts.tests.UserAuthenticationTest.test_register_user_success
```

### Test Coverage
Tests include:
- User registration success and validation
- User login success and validation
- Dashboard access control
- Logout functionality
- Duplicate email prevention
- Password mismatch handling
- Invalid credentials handling

## 🎨 Frontend Technology

- **HTML5**: Semantic markup
- **Bootstrap 5**: Responsive CSS framework
- **Django Templates**: Server-side rendering
- **CSS3**: Custom styling for auth pages

## 🔧 Configuration

Key settings in `inventory_app/settings.py`:

```python
# Installed apps
INSTALLED_APPS = [
    ...
    'accounts',
]

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Message tags for Bootstrap styling
MESSAGE_TAGS = {
    'success': 'success',
    'error': 'danger',
    'info': 'info',
    'warning': 'warning',
}
```

## 💾 Database

- **Type**: SQLite (default for development)
- **Models Used**: Django's built-in User model
- **Tables Created**: 
  - auth_user (user accounts)
  - auth_group (user groups)
  - auth_permission (permissions)
  - Various other auth-related tables

## 🔒 Security Features

1. **Password Hashing**: PBKDF2 with SHA256
2. **CSRF Protection**: Token-based CSRF prevention
3. **SQL Injection Prevention**: Django ORM parameterized queries
4. **XSS Protection**: Django template auto-escaping
5. **Clickjacking Protection**: X-Frame-Options header
6. **Session Security**: Secure session cookies

## 📚 Key Technologies

- **Django 5.2.8**: Web framework
- **Python 3.8+**: Programming language
- **SQLite**: Database
- **Bootstrap 5**: Frontend framework
- **Django Templates**: Template engine

## 🛠️ Development Commands

```bash
# Run development server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run tests
python manage.py test

# Collect static files (production)
python manage.py collectstatic
```

## 📦 Dependencies

- Django 5.2.8 (Web framework)

All dependencies are listed in `requirements.txt`

## 🐛 Troubleshooting

### Issue: "No module named 'accounts'"
**Solution**: Ensure `'accounts'` is in `INSTALLED_APPS` in settings.py

### Issue: "Port 8000 already in use"
**Solution**: Run on different port:
```bash
python manage.py runserver 8001
```

### Issue: Database locked
**Solution**: Delete `db.sqlite3` and re-run migrations:
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue: Static files not loading
**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput
```

## 🚧 Future Enhancements

- [ ] Email verification system
- [ ] Password reset functionality
- [ ] Social authentication (Google, GitHub)
- [ ] Two-factor authentication (2FA)
- [ ] User profile customization
- [ ] Account deletion
- [ ] Activity logging
- [ ] Role-based access control (RBAC)
- [ ] Inventory management features
- [ ] Item management in inventories
- [ ] Search and filter functionality
- [ ] API endpoints (REST/GraphQL)
- [ ] Mobile app support
- [ ] Real-time notifications

## 📄 License

This project is for educational purposes.

## 👨‍💻 Development Tips

1. **Use Django Debug Toolbar**: Great for debugging queries
2. **Keep secrets in environment variables**: Use `python-dotenv`
3. **Write tests as you code**: Easier to catch bugs early
4. **Use Django's ORM**: Avoid raw SQL when possible
5. **Follow PEP 8**: Python style guide

## 📞 Support

For issues or questions, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md)

---

**Happy Coding! 🎉**
