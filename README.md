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

### Docker Services Architecture

```
┌─────────────────────────────────────────────┐
│         Docker Compose Services             │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │  Web Service (Django)                │  │
│  │  - Port: 8000                        │  │
│  │  - Container: inventory_app_web      │  │
│  │  - Image: Built from Dockerfile      │  │
│  └──────────────────────────────────────┘  │
│              ↓ connects to                  │
│  ┌──────────────────────────────────────┐  │
│  │  Database Service (PostgreSQL 16)    │  │
│  │  - Port: 5432                        │  │
│  │  - Container: inventory_app_db       │  │
│  │  - Image: postgres:16-alpine         │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  Volumes:                                   │
│  - postgres_data: Database persistence    │
│  - media_volume: Uploaded images           │
│                                             │
└─────────────────────────────────────────────┘
```

### Data Persistence

- **PostgreSQL Data**: Stored in `postgres_data` volume
- **Media Files**: Stored in `media_volume` (user uploads, receipts, images)
- **Static Files**: Generated at startup, can be regenerated

### Troubleshooting Docker

**Issue: Port 8000 already in use**
```bash
# Change port in docker-compose.yml:
# ports:
#   - "8001:8000"  # Use 8001 instead
docker-compose up -d
```

**Issue: Database connection failed**
```bash
# Ensure database service is running
docker-compose ps

# Check database logs
docker-compose logs db

# Restart database service
docker-compose restart db
```

**Issue: Static files not loading**
```bash
# Rebuild and collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

**Issue: Permission denied on volumes**
```bash
# Fix volume permissions
docker-compose down
docker volume rm inventory_app_media_volume
docker-compose up -d
```

### Docker Security Notes

⚠️ **For Development Only**: The default `.env` values are suitable for development. For production:

1. Use strong `SECRET_KEY` (not the default)
2. Set `DEBUG=False`
3. Use environment-specific `ALLOWED_HOSTS`
4. Use strong `DB_PASSWORD`
5. Consider using secrets management tools

## 📁 Project Structure

```
inventory_app/
├── accounts/                      # Main application
│   ├── migrations/               # Database migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_category_item_activitylog.py
│   │   ├── 0003_delete_activitylog.py
│   │   ├── 0004_receipt.py       # Receipt model creation
│   │   ├── 0005_alter_receipt_options_remove_receipt_date.py
│   │   └── 0006_remove_receipt_created_at_alter_receipt_options_alter_receipt_date.py
│   ├── templates/accounts/       # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── register.html        # Registration page
│   │   ├── login.html           # Login page
│   │   ├── dashboard.html       # User dashboard
│   │   ├── inventory_detail.html # Inventory detail page
│   │   ├── inventory_management.html
│   │   ├── receipt_gallery.html # Receipt management UI
│   │   ├── settings.html        # User settings page
│   │   └── user_profile.html
│   ├── tests/                   # Test modules
│   │   ├── test_backend.py      # Backend tests (42 tests)
│   │   └── test_frontend.py     # Frontend tests (45 tests)
│   ├── forms.py                 # Forms (registration, login)
│   ├── models.py                # Database models
│   │   ├── Inventory model
│   │   ├── Category model
│   │   ├── Item model
│   │   └── Receipt model
│   ├── urls.py                  # URL routing
│   ├── utils.py                 # Utility functions
│   ├── validators.py            # Custom validators
│   └── views.py                 # View functions (700+ lines)
├── inventory_app/               # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
├── media/                       # User-uploaded files
│   ├── item_images/            # Item images
│   ├── receipts/               # Receipt images
│   └── cache/                  # Image thumbnails
├── staticfiles/                 # Compiled static files
├── Dockerfile                   # Docker image definition
├── docker-compose.yml          # Docker compose configuration
├── start.sh                    # Docker startup script
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── nginx.conf                  # Nginx web server config
├── test_receipt_integration.py # Integration tests (7 tests)
└── Documentation/
    ├── AUTHENTICATION_SETUP.md
    ├── PROJECT_DOCUMENTATION.md
    ├── IMPLEMENTATION_SUMMARY.md
    ├── DATABASE_SETUP.md
    ├── QUICK_START_GUIDE.md
    ├── CI_CD_TESTING_SUMMARY.md
    ├── CLOUD_DEPLOYMENT.md
    └── README.md                # This file
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

### Authentication Routes

| Route | Method | Purpose | Auth Required |
|-------|--------|---------|---|
| `/` | GET | Home (redirects to login) | No |
| `/accounts/register/` | GET, POST | User registration | No |
| `/accounts/login/` | GET, POST | User login | No |
| `/accounts/logout/` | GET | User logout | ✓ Yes |
| `/admin/` | GET | Django admin panel | ✓ Superuser |

### Inventory & Item Routes

| Route | Method | Purpose | Auth Required |
|-------|--------|---------|---|
| `/accounts/inventories/` | GET | Dashboard - list inventories | ✓ Yes |
| `/accounts/inventories/create/` | POST | Create inventory | ✓ Yes |
| `/accounts/inventories/<id>/` | GET | Inventory detail | ✓ Yes |
| `/accounts/inventories/<id>/update/` | POST | Update inventory | ✓ Yes |
| `/accounts/inventories/<id>/delete/` | POST | Delete inventory | ✓ Yes |
| `/accounts/inventories/<id>/items/create/` | POST | Create item | ✓ Yes |
| `/accounts/inventories/<id>/items/<item_id>/update/` | POST | Update item | ✓ Yes |
| `/accounts/inventories/<id>/items/<item_id>/delete/` | POST | Delete item | ✓ Yes |

### Receipt Management Routes

| Route | Method | Purpose | Auth Required |
|-------|--------|---------|---|
| `/accounts/inventories/<id>/receipts/` | GET | Receipt gallery | ✓ Yes |
| `/accounts/inventories/<id>/receipts/create/` | POST | Create receipt | ✓ Yes |
| `/accounts/inventories/<id>/receipts/<receipt_id>/update/` | POST | Update receipt | ✓ Yes |
| `/accounts/inventories/<id>/receipts/<receipt_id>/delete/` | POST | Delete receipt | ✓ Yes |

### User Settings Routes

| Route | Method | Purpose | Auth Required |
|-------|--------|---------|---|
| `/accounts/settings/` | GET, POST | User settings | ✓ Yes |
| `/accounts/change-email/` | POST | Change email | ✓ Yes |
| `/accounts/change-password/` | POST | Change password | ✓ Yes |
| `/accounts/delete-account/` | POST | Delete account | ✓ Yes |

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

## 🤖 AI-Assisted Learning Journey

This project is part of a **student learning experience** where I leveraged AI tools to understand and build a production-ready web application. Here's how AI was integrated into the development process:

### Planning & Architecture
- **GitHub Copilot**: Used for suggesting database schema design and model relationships
- **ChatGPT**: Helped plan the application architecture, feature prioritization, and user workflows
- **Outcome**: Clear understanding of how to structure a Django application with proper separation of concerns

### Implementation & Coding
- **GitHub Copilot**: Provided code suggestions for views, forms, and JavaScript functionality
- **Assisted by**: Real-time code completion for common patterns like CRUD operations
- **Learning**: Reviewed and understood every suggestion, implementing only appropriate solutions
- **Outcome**: 700+ lines of well-structured Django views with proper error handling

### Feature Development
- **Receipt Gallery Feature**: Designed with AI assistance for modal-based UI interactions
- **Date Handling**: Learned how to work with Django DateField and manage date logic
- **Image Uploads**: Implemented with Sorl-Thumbnail for optimization
- **Access Control**: Built proper permission checking to prevent cross-user access

### Database Design
- **Relationships**: ForeignKey relationships for Inventory → Items → Receipt structure
- **Migrations**: Understood Django's migration system for schema evolution
- **Learning**: Created 6 migrations to refactor and improve the data model

### Testing & Quality Assurance
- **ChatGPT**: Helped design comprehensive test cases covering user flows
- **GitHub Copilot**: Suggested test structures and assertions
- **Result**: 94 passing tests with 42 backend, 45 frontend, and 7 integration tests

### Deployment & DevOps
- **Docker**: Created containerized deployment with PostgreSQL
- **Docker Compose**: Orchestrated multi-container applications
- **Google Cloud Run**: Deployed with environment-specific configurations
- **CI/CD**: Implemented automated testing pipelines
- **Learning**: Understood containerization, environment variables, and cloud deployment

### Key Learning Outcomes

1. **Full-Stack Development**: From database design to frontend interactions
2. **Django Framework**: Models, views, templates, forms, and ORM queries
3. **Frontend Technologies**: Bootstrap 5, vanilla JavaScript, modal interactions
4. **Database Management**: PostgreSQL, migrations, data relationships
5. **DevOps & Deployment**: Docker, Docker Compose, cloud platforms
6. **Testing**: Unit tests, integration tests, test coverage
7. **Version Control**: Git workflows, code organization, documentation

### How to Learn From This Project

This codebase is designed to be educational:

- **Read the code**: Every file is commented and follows Django best practices
- **Check the tests**: Tests show how each feature is supposed to work
- **Follow the commits**: Git history shows the evolution of features
- **Review migrations**: See how the database schema evolved
- **Study the templates**: HTML templates demonstrate template tags and forms
- **Examine the views**: Views show proper authentication, validation, and error handling

### AI Tool Limitations & When to Think Critically

While AI was helpful, I learned when **not** to use AI suggestions:

- ❌ Don't copy-paste without understanding
- ❌ Don't accept security suggestions without review
- ❌ Don't ignore test failures in favor of "working" code
- ❌ Don't skip documentation or comments
- ✅ **Do verify**: Every suggestion against documentation
- ✅ **Do test**: Changes before deploying
- ✅ **Do understand**: Why a solution works, not just that it works
- ✅ **Do refactor**: When AI suggestions need improvement

### Resources Used

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Stack Overflow and open-source projects

### For Other Students

If you're learning web development:

1. **Start small**: Build basic features before complex ones
2. **Use AI wisely**: Let it suggest, but you decide
3. **Test everything**: Don't rely on code that isn't tested
4. **Document your learning**: Comments help future-you understand
5. **Deploy early**: Understanding deployment is crucial
6. **Read others' code**: Learn patterns from established projects

---

## 🤝 Contributing

This is a student learning project. Feel free to fork and contribute!

## 🔧 Environment Variables

### Development (`.env` file for Docker)

```env
# Django Settings
DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_PASSWORD=devpass123

# Server
PORT=8000
```

### Production (set in deployment platform)

```env
# Django Settings
DEBUG=False
SECRET_KEY=<generated-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://user:password@host:port/dbname

# Storage
STATIC_URL=/static/
MEDIA_URL=/media/

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### To Generate Django SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📄 License

This project is for educational purposes.

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

**Docker Issues**
- Run `docker-compose down` and `docker-compose up -d` to restart services
- Check logs with `docker-compose logs -f`
- Ensure Docker Desktop is running (Windows/Mac)

**Database Issues**
- PostgreSQL might be running on port 5432; change in docker-compose.yml if needed
- Run migrations with `docker-compose exec web python manage.py migrate`
- Reset database with `docker-compose down -v` (warning: deletes all data)

**Static Files**
- Run `python manage.py collectstatic` in development
- Run `docker-compose exec web python manage.py collectstatic --noinput` in Docker

### Getting Help

- **Django Docs**: https://docs.djangoproject.com/
- **Docker Docs**: https://docs.docker.com/
- **Stack Overflow**: Tag your questions with `django`, `docker`, `python`
- **GitHub Issues**: Create an issue in this repository

## 📦 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.8+ | 3.13+ |
| Django | 5.2+ | 5.2.8 |
| PostgreSQL | 13+ | 16+ |
| Docker | 20.10+ | Latest |
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 2GB+ |

## 🔄 Project Status

- ✅ Core Features: Complete
- ✅ User Authentication: Complete
- ✅ Inventory Management: Complete
- ✅ Receipt Gallery: Complete
- ✅ Docker Support: Complete
- ✅ Testing: 94 tests passing
- 🚀 Deployment: Ready for production
- 📚 Documentation: Comprehensive

---

**Current Version**: 1.0.0  
**Django Version**: 5.2.8  
**Python Version**: 3.13+  
**Last Updated**: December 7, 2025