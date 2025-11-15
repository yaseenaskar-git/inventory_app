# Database Setup Instructions

## Overview
This document explains how to set up the database for the inventory management system.

## Database Type
The application uses **SQLite** by default, which is perfect for development. The database file is stored as `db.sqlite3` in the project root.

## Initial Setup

### Step 1: Run Migrations
Migrations apply the database schema to create all necessary tables.

```bash
python manage.py migrate
```

This command will:
- Apply all pending migrations
- Create the `db.sqlite3` file (if it doesn't exist)
- Create all Django's built-in tables including:
  - `auth_user` - User accounts
  - `auth_group` - User groups
  - `auth_permission` - Permission definitions
  - `django_session` - Session data
  - `django_admin_log` - Admin action logs
  - And other Django framework tables

### Step 2: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```

You'll be prompted for:
- Email (or username)
- Password
- Confirm password

Example:
```
Email: admin@example.com
Password: ▓▓▓▓▓▓▓▓
Password (again): ▓▓▓▓▓▓▓▓
Superuser created successfully.
```

This account is for accessing the Django admin panel at `/admin/`

## Understanding Migrations

### What are Migrations?
Migrations are files that describe changes to the database schema. They track:
- New tables created
- Fields added/removed
- Constraints added/removed
- Data transformations

### Key Migration Commands

```bash
# See all migrations
python manage.py showmigrations

# Apply a specific migration
python manage.py migrate accounts 0001

# Rollback last migration
python manage.py migrate accounts 0000

# Create new migrations (when you add new models)
python manage.py makemigrations

# Show SQL for a migration without applying it
python manage.py sqlmigrate accounts 0001
```

## Database Schema

### Users Table (auth_user)
```
┌─────────────┬─────────┬──────────────┐
│   Column    │  Type   │   Constraints│
├─────────────┼─────────┼──────────────┤
│ id          │ INTEGER │ PRIMARY KEY  │
│ username    │ VARCHAR │ UNIQUE       │
│ email       │ VARCHAR │ UNIQUE       │
│ password    │ VARCHAR │              │
│ first_name  │ VARCHAR │              │
│ last_name   │ VARCHAR │              │
│ is_active   │ BOOLEAN │ DEFAULT TRUE │
│ is_staff    │ BOOLEAN │              │
│ is_superuser│ BOOLEAN │              │
│ date_joined │ DATETIME│              │
│ last_login  │ DATETIME│ NULL         │
└─────────────┴─────────┴──────────────┘
```

### Sessions Table (django_session)
```
┌────────────────┬─────────┬──────────────┐
│    Column      │  Type   │   Constraints│
├────────────────┼─────────┼──────────────┤
│ session_key    │ VARCHAR │ PRIMARY KEY  │
│ session_data   │ TEXT    │              │
│ expire_date    │ DATETIME│ INDEXED      │
└────────────────┴─────────┴──────────────┘
```

## Backup and Restore

### Backup Database
```bash
# Copy the database file
cp db.sqlite3 db.sqlite3.backup
# or on Windows
copy db.sqlite3 db.sqlite3.backup
```

### Restore Database
```bash
# Restore from backup
cp db.sqlite3.backup db.sqlite3
# or on Windows
copy db.sqlite3.backup db.sqlite3
```

## Reset Database (Development Only)

### Complete Reset
```bash
# Delete the database file
rm db.sqlite3
# or on Windows
del db.sqlite3

# Re-run migrations
python manage.py migrate

# Create new superuser
python manage.py createsuperuser
```

### Clear All Data (Keep Schema)
```bash
python manage.py flush
```

This will delete all data but keep the tables intact.

## Access Database Directly

### Using Django Shell
```bash
python manage.py shell
```

```python
# Import models
from django.contrib.auth.models import User

# Query users
users = User.objects.all()
for user in users:
    print(f"{user.email}: {user.username}")

# Create user
user = User.objects.create_user(
    username='test@example.com',
    email='test@example.com',
    password='TestPassword123'
)

# Get specific user
user = User.objects.get(email='test@example.com')

# Update user
user.first_name = 'John'
user.save()

# Delete user
user.delete()

# Check if user exists
exists = User.objects.filter(email='test@example.com').exists()
```

### Using SQLite Browser
Download and install [DB Browser for SQLite](https://sqlitebrowser.org/)

Then open `db.sqlite3` file to browse tables directly.

## Common Issues and Solutions

### Issue: "DatabaseError: table auth_user already exists"
**Cause**: Migrations already applied
**Solution**: This is normal if you've already migrated

### Issue: "UNIQUE constraint failed: auth_user.email"
**Cause**: Trying to create user with duplicate email
**Solution**: Use different email or delete existing user

### Issue: Database is locked
**Cause**: Another process is accessing the database
**Solution**: 
```bash
# Make sure no other process is running Django
# Kill any running servers
# Delete database and restart
rm db.sqlite3
python manage.py migrate
```

### Issue: Foreign key constraint failed
**Cause**: Trying to delete a user with related data
**Solution**: Delete related data first or use cascade delete

## Testing Database Operations

### Run Tests
```bash
python manage.py test accounts
```

Tests automatically:
- Create a test database
- Apply migrations
- Run tests
- Delete test database

## Production Considerations

### For Production Deployment:
- Switch from SQLite to PostgreSQL or MySQL
- Use managed database service (AWS RDS, Heroku, etc.)
- Implement database backups
- Use connection pooling
- Implement database monitoring
- Use environment variables for credentials
- Enable SSL connections
- Set up read replicas for scaling

### Update settings.py for Production
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventory_db',
        'USER': 'db_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}
```

## Data Types Reference

| Django Type | SQLite Type | Size |
|-------------|-------------|------|
| CharField | VARCHAR | Variable |
| IntegerField | INTEGER | 4 bytes |
| BigIntegerField | BIGINT | 8 bytes |
| TextField | TEXT | Variable |
| BooleanField | BOOLEAN | 1 byte |
| DateTimeField | DATETIME | 8 bytes |
| DateField | DATE | 3 bytes |
| TimeField | TIME | 3 bytes |
| EmailField | VARCHAR | Variable |
| URLField | VARCHAR | Variable |

## Optimization Tips

1. **Add Indexes**: For frequently queried fields
   ```python
   class Meta:
       indexes = [
           models.Index(fields=['email']),
       ]
   ```

2. **Use Select Related**: For foreign key lookups
   ```python
   users = User.objects.select_related('profile')
   ```

3. **Use Prefetch Related**: For reverse relations
   ```python
   users = User.objects.prefetch_related('groups')
   ```

4. **Limit Queries**: Use slicing
   ```python
   users = User.objects.all()[:100]
   ```

5. **Use Only/Defer**: Select specific fields
   ```python
   users = User.objects.only('email', 'username')
   ```

## Documentation Links
- [Django Migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/)
- [Django ORM](https://docs.djangoproject.com/en/5.2/topics/db/)
- [SQLite Documentation](https://www.sqlite.org/lang.html)
