# Inventory App

A Django-based inventory management application for tracking items, managing inventories, and organizing personal or business stock with user authentication and image uploads.

## 📊 Technology Stack

### Backend
- **Framework**: Django 5.2.8
- **Language**: Python 3.13
- **Server**: Django Development Server / Gunicorn
- **Authentication**: Django built-in auth system with custom password validation

### Frontend
- **HTML/Template Engine**: Django Templates (HTML5)
- **Styling**: Bootstrap 5 CSS Framework
- **JavaScript**: Vanilla JavaScript (event delegation)
- **Image Processing**: Sorl-Thumbnail for image optimization

### Database
- **Development**: SQLite3
- **Production**: PostgreSQL 16
- **ORM**: Django ORM

### APIs & Libraries
- **Image Processing**: Pillow 12.0.0
- **Thumbnail Generation**: sorl-thumbnail 12.9.0
- **Database Adapter**: psycopg2-binary (PostgreSQL)
- **Container**: Docker & Docker Compose
- **Cloud**: Google Cloud Run

## ✨ Main Features

### 1. **User Authentication**
- ✅ Secure user registration with email
- ✅ Strong password validation (8+ chars, uppercase, lowercase, digit, special char)
- ✅ User login/logout with session management
- ✅ Protected dashboard and settings pages

### 2. **Inventory Management**
- ✅ Create and manage multiple inventories
- ✅ Organize items within inventories
- ✅ Add/Edit/Delete items
- ✅ Track item quantities with +/- buttons

### 3. **Item Management**
- ✅ Item name, brand, description, quantity
- ✅ Expiration date tracking
- ✅ Image uploads with thumbnail generation
- ✅ Low stock alerts (≤3 items)
- ✅ Expiring soon badges (≤7 days)

### 4. **Sorting & Filtering**
- ✅ Sort by expiration date (soon → late / late → soon)
- ✅ Sort by quantity (low → high / high → low)
- ✅ Pagination for large item lists

### 5. **User Settings**
- ✅ Change email address
- ✅ Change password with strong validation
- ✅ Delete account (API endpoint)

## 🚀 How to Run in Web Browser

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- Git

### Quick Start (4 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/yaseenaskar-git/inventory_app.git
cd inventory_app

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database and start server
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Access the Application
- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Login Page**: http://localhost:8000/accounts/login

### Common Commands

```bash
# Start development server
python manage.py runserver

# Run all tests
python manage.py test accounts

# Create superuser
python manage.py createsuperuser

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

## 🐳 How to Run with Docker

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### Quick Start (3 Commands)

```bash
# 1. Clone and setup
git clone https://github.com/yaseenaskar-git/inventory_app.git
cd inventory_app
cp .env.example .env

# 2. Build and run
docker-compose build
docker-compose up -d

# 3. Initialize database
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### Access the Application
- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

### Common Docker Commands

```bash
# View logs
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Stop services
docker-compose down

# Rebuild images
docker-compose build --no-cache
```

### Docker Services
- **Web**: Django app on port 8000
- **Database**: PostgreSQL on port 5432
- **Media Volume**: Stores uploaded images
- **Database Volume**: Persistent PostgreSQL data

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

**Django Version**: 5.2.8
**Python Version**: 3.8+