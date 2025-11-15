# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Setup Issues

#### Issue: "No module named 'django'"
**Error Message**: `ModuleNotFoundError: No module named 'django'`

**Causes**: Django not installed in virtual environment

**Solutions**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Install Django
pip install -r requirements.txt
```

---

#### Issue: "No module named 'accounts'"
**Error Message**: `ModuleNotFoundError: No module named 'accounts'`

**Causes**: 
- App not added to `INSTALLED_APPS`
- Wrong app name

**Solutions**:
1. Check `inventory_app/settings.py`
2. Ensure `'accounts'` is in `INSTALLED_APPS`
3. Check directory structure:
   ```
   accounts/
   ├── __init__.py  (must exist)
   ├── apps.py
   ├── models.py
   └── ...
   ```

---

#### Issue: "Port 8000 already in use"
**Error Message**: `Address already in use`

**Causes**: Another application using port 8000

**Solutions**:
```bash
# Use different port
python manage.py runserver 8001

# Find and kill process using port 8000 (macOS/Linux)
lsof -ti:8000 | xargs kill -9

# Find and kill process using port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### 🔴 Database Issues

#### Issue: "No such table: auth_user"
**Error Message**: `OperationalError: no such table: auth_user`

**Causes**: Migrations not run

**Solutions**:
```bash
# Run migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

---

#### Issue: "UNIQUE constraint failed: auth_user.email"
**Error Message**: `IntegrityError: UNIQUE constraint failed: auth_user.email`

**Causes**: Trying to create user with email that already exists

**Solutions**:
```bash
# Use different email
# OR
# Delete the user with that email:
python manage.py shell
from django.contrib.auth.models import User
User.objects.filter(email='existing@email.com').delete()
exit()
```

---

#### Issue: "database is locked"
**Error Message**: `OperationalError: database is locked`

**Causes**: 
- Multiple Django processes running
- Database file permissions issue
- Another application accessing database

**Solutions**:
```bash
# Stop all running Django servers (Ctrl+C in terminal)

# If still locked, reset database (development only)
rm db.sqlite3  # macOS/Linux
del db.sqlite3  # Windows

# Re-run migrations
python manage.py migrate
```

---

### 🔴 Authentication Issues

#### Issue: "User cannot login"
**Symptoms**: Login fails with "Invalid email or password"

**Causes**:
- Wrong email/password combination
- User doesn't exist
- Password was changed

**Solutions**:
```bash
# Verify user exists
python manage.py shell
from django.contrib.auth.models import User
users = User.objects.all()
for user in users:
    print(user.email, user.username)

# Reset password if needed
python manage.py shell
from django.contrib.auth.models import User
user = User.objects.get(email='test@example.com')
user.set_password('NewPassword123')
user.save()
exit()
```

---

#### Issue: "Dashboard shows 'Page not found'"
**Error Message**: `404 - Not Found`

**Causes**: URL not registered correctly

**Solutions**:
1. Check `accounts/urls.py` has:
   ```python
   path('dashboard/', views.dashboard, name='dashboard'),
   ```
2. Check `inventory_app/urls.py` includes:
   ```python
   path('accounts/', include('accounts.urls')),
   ```
3. Check view exists in `accounts/views.py`

---

#### Issue: "Login redirects to itself"
**Symptoms**: After logging in, redirected back to login page

**Causes**: 
- LOGIN_REDIRECT_URL not set
- Wrong redirect URL

**Solutions**:
Check `inventory_app/settings.py`:
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'  # Should match url name
LOGOUT_REDIRECT_URL = 'login'
```

---

### 🔴 Template Issues

#### Issue: "Bootstrap styling not working"
**Symptoms**: Page looks unstyled, no colors/layout

**Causes**: 
- Bootstrap CDN not loading
- Internet connection issue
- Browser cache issue

**Solutions**:
1. Check internet connection
2. Clear browser cache:
   - Ctrl+Shift+Delete (Windows/Linux)
   - Cmd+Shift+Delete (macOS)
3. Try different browser

---

#### Issue: "CSRF token missing"
**Error Message**: `Forbidden (403): CSRF token missing`

**Causes**: Form missing `{% csrf_token %}`

**Solutions**:
Add to all form templates:
```html
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

#### Issue: "Form not displaying"
**Symptoms**: Blank form or form fields not showing

**Causes**:
- Form not passed to template
- Template syntax error
- Form not initialized

**Solutions**:
1. Check view passes form:
   ```python
   return render(request, 'template.html', {'form': form})
   ```
2. Check template renders form:
   ```html
   {{ form.email }}
   {{ form.password }}
   ```
3. Check form fields in `accounts/forms.py`

---

### 🔴 Email Issues

#### Issue: "Email validation failing"
**Error Message**: Form shows "Enter a valid email address"

**Causes**: Invalid email format

**Solutions**:
Use valid email format:
```
✓ user@example.com
✓ name.surname@example.com
✗ user@example (missing domain)
✗ @example.com (missing username)
```

---

### 🔴 Password Issues

#### Issue: "Password too weak"
**Error Message**: "This password is too common" or similar

**Causes**: Password fails validation

**Solutions**:
Use stronger password:
- At least 8 characters
- Mix of letters, numbers, symbols
- Not all numbers
- Not common words

```
✓ MySecurePass123!
✓ Inventory@2024
✗ 12345678 (all numbers)
✗ password (common word)
```

---

#### Issue: "Passwords don't match"
**Error Message**: "The two password fields didn't match"

**Causes**: Password and confirmation don't match

**Solutions**:
Ensure both password fields match:
1. Type carefully
2. Show password to verify
3. Copy-paste to ensure accuracy

---

### 🔴 Testing Issues

#### Issue: "Tests fail: 'test_register_page_loads'"
**Error Message**: `AssertionError: False is not true`

**Causes**: 
- View not found
- URL not registered
- Template not found

**Solutions**:
```bash
# Run specific test with verbose output
python manage.py test accounts.tests.UserAuthenticationTest.test_register_page_loads -v 2

# Check URL routing
python manage.py show_urls

# Verify all files exist
```

---

### 🔴 Performance Issues

#### Issue: "Slow page load"
**Symptoms**: Pages take long time to load

**Causes**:
- Large database queries
- Missing indexes
- Excessive template rendering

**Solutions**:
```bash
# Run Django Debug Toolbar
pip install django-debug-toolbar

# Check query count
# Use select_related/prefetch_related for queries
# Minimize template processing
```

---

### 🔴 Static Files Issues

#### Issue: "CSS not loading in production"
**Symptoms**: Page displays but styling missing

**Causes**: Static files not collected

**Solutions**:
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_URL in settings
STATIC_URL = '/static/'

# Check STATIC_ROOT set for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

---

## 🔧 Debug Mode

### Enable Debug Output
```python
# In settings.py
DEBUG = True  # ONLY in development!
```

### Django Shell for Debugging
```bash
python manage.py shell
```

```python
# Query users
from django.contrib.auth.models import User
User.objects.all()

# Get specific user
User.objects.get(email='test@example.com')

# Create test user
User.objects.create_user(
    username='test@example.com',
    email='test@example.com',
    password='TestPassword123'
)

# Delete user
user.delete()

# Check authentication
from django.contrib.auth import authenticate
user = authenticate(username='test@example.com', password='TestPassword123')
print(user)  # None if failed
```

---

## 📋 Debugging Checklist

When something doesn't work:

1. **Check Error Message**
   - Read the full error carefully
   - Note the file and line number

2. **Check Console Output**
   - Look for warnings
   - Check server logs

3. **Verify Setup**
   - Migrations run: `python manage.py showmigrations`
   - App installed: Check `INSTALLED_APPS`
   - URLs registered: Check `urls.py` files

4. **Check Database**
   - Tables exist: `python manage.py shell` then query
   - Data exists: Check user count
   - No corruption: Try reset

5. **Check Files**
   - Templates exist
   - Views exist
   - URLs match view names
   - All imports correct

6. **Clear Cache**
   - Browser cache
   - Django cache (if configured)
   - Python cache (`__pycache__`)

---

## 🆘 Getting Help

### Before Asking for Help

1. Run all tests:
   ```bash
   python manage.py test accounts
   ```

2. Check logs:
   ```bash
   python manage.py runserver > debug.log 2>&1
   ```

3. Try fresh installation:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/django)
- [Django Forums](https://forum.djangoproject.com/)

---

## 📞 Report Issue

When reporting issues, include:

1. **Error message** (full text)
2. **Steps to reproduce**
3. **Expected behavior**
4. **Actual behavior**
5. **Your setup**:
   - Python version: `python --version`
   - Django version: `python -m django --version`
   - OS: Windows/macOS/Linux

---

**Happy debugging! 🐛**
