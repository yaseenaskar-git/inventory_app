# Inventory App

A full-stack Django inventory management application for tracking items, managing inventories, receipts, and organizing personal or business stock with user authentication, image uploads, and Docker containerization support.

## 🎓 About This Project

This is a **student learning project** created with the assistance of AI tools to understand full-stack web development, database design, and cloud deployment concepts. Throughout the development process, I used **GitHub Copilot** and **ChatGPT** to:

- **Plan** the application architecture and database schema
- **Design** user workflows and interface components
- **Implement** backend logic and frontend features
- **Debug** issues and optimize code
- **Deploy** the application to production using Docker and Google Cloud Run

This project demonstrates how AI can be a powerful learning companion for students building real-world applications while maintaining code quality and understanding fundamental concepts.

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

### 5. **Receipt Gallery & Management**
- ✅ Upload and store receipts with images
- ✅ Manually set receipt dates
- ✅ View receipt details in modal
- ✅ Edit receipt name, description, and date
- ✅ Delete receipts and associated images
- ✅ Organized by inventory with date sorting

### 6. **User Settings**
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

### Step 1: Clone Repository

```bash
git clone https://github.com/yaseenaskar-git/inventory_app.git
cd inventory_app
```

### Step 2: Configure Environment

Create a `.env` file in the project root with the following variables:

```bash
# Django Configuration
DEBUG=False
SECRET_KEY=your-secret-key-here-generate-with-django-settings
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_PASSWORD=your-secure-db-password-here

# Port Configuration
PORT=8000
```

**To generate a Django SECRET_KEY**, run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Build Docker Images

```bash
docker-compose build
```

This will:
- Build the Django web service image
- Pull and prepare the PostgreSQL database image
- Install all Python dependencies

### Step 4: Start Services

```bash
docker-compose up -d
```

This starts both the web service and PostgreSQL database in the background.

### Step 5: Initialize Database

```bash
# Create database migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser (admin account)
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Access the Application
- **Web App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API**: http://localhost:8000/api/

### Common Docker Commands

```bash
# View logs from all services
docker-compose logs -f

# View logs from specific service (web or db)
docker-compose logs -f web

# Access Django shell
docker-compose exec web python manage.py shell

# Run Django management commands
docker-compose exec web python manage.py <command>

# Stop all services (keeps data in volumes)
docker-compose down

# Stop and remove all containers/volumes (WARNING: deletes data)
docker-compose down -v

# Rebuild images (useful after dependency changes)
docker-compose build --no-cache

# Restart services
docker-compose restart

# View service status
docker-compose ps

# Execute command in running container
docker-compose exec web bash
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

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test accounts test_receipt_integration

# Run specific test module
python manage.py test accounts.tests.test_backend
python manage.py test accounts.tests.test_frontend
python manage.py test test_receipt_integration

# Run tests with verbose output
python manage.py test accounts -v 2

# Run with coverage
coverage run --source='accounts' manage.py test accounts
coverage report
```

### Test Coverage

**Total Tests**: 94 tests passing ✅

- **Backend Tests** (42 tests):
  - User authentication (registration, login, logout, password validation)
  - Inventory management (create, read, update, delete)
  - Item management (CRUD operations, stock tracking)
  - Expiration date alerts and low stock warnings
  - Access control and security

- **Frontend Tests** (45 tests):
  - Dashboard rendering
  - Form validation
  - Modal interactions
  - JavaScript functionality

- **Integration Tests** (7 tests):
  - Receipt gallery page loading
  - Receipt creation with/without images
  - Receipt editing and updating
  - Receipt deletion
  - Cross-user access control

### Running Tests in Docker

```bash
# Run tests inside Docker container
docker-compose exec web python manage.py test accounts

# Run with verbose output
docker-compose exec web python manage.py test accounts -v 2
```

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
## 📋 Common Commands

### Development Server

```bash
# Start development server
python manage.py runserver

# Start on specific port
python manage.py runserver 0.0.0.0:8080
```

### Database Management

```bash
# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Apply migrations to specific app
python manage.py migrate accounts

# Show migration status
python manage.py showmigrations

# Rollback last migration
python manage.py migrate accounts 0004
```

### Testing

```bash
# Run all tests
python manage.py test accounts test_receipt_integration

# Run specific test module
python manage.py test accounts.tests.test_backend

# Run with verbose output
python manage.py test accounts -v 2

# Run specific test class
python manage.py test accounts.tests.test_backend.InventoryManagementTests
```

### Django Admin & Users

```bash
# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Change user password
python manage.py changepassword username
```

### Static Files & Media

```bash
# Collect static files
python manage.py collectstatic

# Collect without prompt
python manage.py collectstatic --noinput

# Clear cache
python manage.py clear_cache
```

### Utility Commands

```bash
# Check for issues
python manage.py check

# Show installed apps
python manage.py showmigrations

# Load fixture data
python manage.py loaddata fixture_name

# Create fixture from data
python manage.py dumpdata > data.json
```

### Database Reset (Development Only ⚠️)

```bash
# Remove database file
rm db.sqlite3

# Recreate database
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser
```

## 📞 Support & Troubleshooting

### Setup Issues

1. **Check Troubleshooting Guide**: [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
2. **Review Setup Docs**: [AUTHENTICATION_SETUP.md](./AUTHENTICATION_SETUP.md)
3. **See Project Details**: [PROJECT_DOCUMENTATION.md](./PROJECT_DOCUMENTATION.md)
4. **Quick Reference**: [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md)

### Common Issues

**Python/Virtual Environment**
- Ensure Python 3.13+ is installed
- Activate virtual environment before running commands
- Run `pip install -r requirements.txt` if missing packages

## 📦 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8+ | 3.13+ |
| Django | 5.2+ | 5.2.8 |
| PostgreSQL | 13+ | 16+ |
| Docker | 20.10+ | Latest |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 2GB+ |

---

**Current Version**: 1.0.0  
**Django Version**: 5.2.8  
**Python Version**: 3.13+  
**Last Updated**: December 7, 2025