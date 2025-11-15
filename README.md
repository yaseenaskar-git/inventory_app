# Inventory Management System

A Django-based inventory management application with secure user authentication, allowing users to create accounts, manage inventories, and track items.

## 🎯 Current Status: Phase 1 - Authentication Complete ✅

### ✨ Features Implemented

#### User Authentication (COMPLETE)
- ✅ **User Registration**: Email-based account creation with secure password hashing
- ✅ **User Login**: Secure credential verification with session management
- ✅ **User Logout**: Secure session termination
- ✅ **Dashboard**: Protected user dashboard with personalized content
- ✅ **Access Control**: Authentication-required routes using `@login_required`
- ✅ **Error Handling**: User-friendly error messages for validation failures
- ✅ **Responsive UI**: Bootstrap 5 styling for mobile-friendly interface
- ✅ **CSRF Protection**: Token-based security on all forms
- ✅ **Password Security**: PBKDF2 hashing with strength validation

## 📋 Technology Stack

- **Backend**: Python 3.8+, Django 5.2.8
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Database**: SQLite3 (Development)
- **Authentication**: Django's built-in auth system
- **Testing**: Django TestCase framework

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup (3 steps)

**Option 1: Automated Setup (Recommended)**
```bash
# Windows
setup.bat

# macOS/Linux
bash setup.sh
```

**Option 2: Manual Setup**
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create admin account
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

### Access the Application
- **Frontend**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## 📁 Project Structure

```
inventory_app/
├── accounts/                  # Authentication app
│   ├── migrations/           # Database migrations
│   ├── templates/accounts/   # HTML templates
│   │   ├── base.html        # Base template
│   │   ├── register.html    # Registration page
│   │   ├── login.html       # Login page
│   │   └── dashboard.html   # User dashboard
│   ├── forms.py             # Registration & login forms
│   ├── models.py            # Database models
│   ├── tests.py             # Unit tests
│   ├── urls.py              # URL routing
│   ├── utils.py             # Utility functions
│   └── views.py             # View functions
├── inventory_app/           # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── Documentation/
    ├── AUTHENTICATION_SETUP.md     # Setup guide
    ├── PROJECT_DOCUMENTATION.md    # Project details
    ├── IMPLEMENTATION_SUMMARY.md   # Implementation details
    ├── DATABASE_SETUP.md           # Database guide
    └── QUICK_START_GUIDE.md        # Quick reference
```

## 🔐 User Workflows

### Registration
1. Navigate to `/accounts/register/`
2. Enter email and password
3. Confirm password
4. Account created and auto-logged in
5. Redirected to dashboard

### Login
1. Navigate to `/accounts/login/`
2. Enter email and password
3. Redirected to dashboard on success

### Logout
1. Click "Logout" button on dashboard
2. Redirected to login page

## 📚 URL Routes

| Route | Purpose | Auth Required |
|-------|---------|---|
| `/` | Home (redirects to login) | No |
| `/accounts/register/` | User registration | No |
| `/accounts/login/` | User login | No |
| `/accounts/logout/` | User logout | ✓ Yes |
| `/accounts/dashboard/` | User dashboard | ✓ Yes |
| `/admin/` | Django admin panel | ✓ Superuser |

## 🧪 Testing

Run the test suite:
```bash
python manage.py test accounts
```

Tests cover:
- User registration and validation
- User login and session management
- Dashboard access control
- Logout functionality
- Error handling

## 📖 Documentation

### Getting Started
- **[QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md)** - Quick reference and checklist

### Setup and Installation
- **[AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md)** - Detailed setup instructions and troubleshooting

### Project Details
- **[PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)** - Complete project overview and architecture

### Implementation Details
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Technical implementation breakdown

### Database
- **[DATABASE_SETUP.md](./DATABASE_SETUP.md)** - Database configuration and migration guide

## 🔒 Security Features

✅ **Password Security**
- PBKDF2 hashing with SHA256
- 8+ character minimum
- Strength validation
- Confirmation required

✅ **CSRF Protection**
- Token-based protection
- On all form submissions

✅ **Input Validation**
- Email format validation
- Email uniqueness check
- Password matching

✅ **Access Control**
- Authentication required for protected routes
- Automatic redirect to login
- Session-based authorization

## 💾 Database

- **Type**: SQLite3 (Development)
- **Location**: `db.sqlite3`
- **Migrations**: Located in `accounts/migrations/`

### Initialize Database
```bash
python manage.py migrate
```

## 🚧 Upcoming Features (Phase 2+)

- [ ] Inventory management system
- [ ] Item tracking per inventory
- [ ] Search and filtering
- [ ] Pagination
- [ ] Bulk operations
- [ ] Export/Import functionality
- [ ] Email notifications
- [ ] User profile customization
- [ ] Activity logging
- [ ] Analytics dashboard
- [ ] REST API endpoints

## 📋 Common Commands

```bash
# Start development server
python manage.py runserver

# Run tests
python manage.py test accounts

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Reset database (development only)
rm db.sqlite3
python manage.py migrate
```

## 🤝 Contributing

This is a personal learning project. Feel free to fork and contribute!

## 📄 License

This project is for educational purposes.

## 📞 Support

For setup issues or questions:
1. Check [AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md) troubleshooting section
2. Review [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)
3. Refer to [Django Documentation](https://docs.djangoproject.com/)

## ✅ Verification Checklist

- [x] User authentication system
- [x] Registration with validation
- [x] Login with session management
- [x] Logout functionality
- [x] Dashboard access control
- [x] Error handling and messages
- [x] Responsive UI design
- [x] Unit tests
- [x] Complete documentation
- [x] Setup scripts

---

**Development Status**: Phase 1 Complete ✅
**Last Updated**: November 15, 2025
**Django Version**: 5.2.8
**Python Version**: 3.8+

Ready to build! 🚀



