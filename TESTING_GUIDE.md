# Automated CI/CD Testing Guide

## Overview
This document covers running automated tests locally and in Google Cloud Build for the Inventory App. Tests are organized into two comprehensive test suites: **Backend Tests** and **Frontend Tests**.

---

## Quick Start

### Run All Tests
```bash
python manage.py test accounts.tests
```

### Run Backend Tests Only
```bash
python manage.py test accounts.tests.test_backend
```

### Run Frontend Tests Only
```bash
python manage.py test accounts.tests.test_frontend
```

### Run Specific Test Class
```bash
python manage.py test accounts.tests.test_backend.UserAuthenticationTests
python manage.py test accounts.tests.test_frontend.FormValidationTests
```

### Run Single Test Method
```bash
python manage.py test accounts.tests.test_backend.UserAuthenticationTests.test_user_registration_valid_data
```

---

## Backend Tests (`test_backend.py`)

Comprehensive backend testing with 60+ test cases covering:

### 1. **User Authentication Tests** (12 tests)
   - ✅ User registration with valid data
   - ✅ Registration with password mismatch
   - ✅ Weak password validation (no uppercase, lowercase, digit, special char)
   - ✅ Duplicate username prevention
   - ✅ Duplicate email prevention
   - ✅ Login with valid credentials
   - ✅ Login with invalid email/password
   - ✅ User logout
   - ✅ Dashboard authentication requirement
   - ✅ Dashboard access for authenticated users

**Run:**
```bash
python manage.py test accounts.tests.test_backend.UserAuthenticationTests
```

### 2. **Inventory Management Tests** (7 tests)
   - ✅ Create inventory with valid data
   - ✅ Prevent duplicate inventory names
   - ✅ Require inventory name
   - ✅ Retrieve user-specific inventories
   - ✅ Delete inventory
   - ✅ Update inventory details
   - ✅ Inventory isolation between users

**Run:**
```bash
python manage.py test accounts.tests.test_backend.InventoryManagementTests
```

### 3. **Item Management Tests** (15 tests)
   - ✅ Create item with valid data
   - ✅ Create item with image upload
   - ✅ Item name requirement
   - ✅ Prevent negative quantity
   - ✅ Low stock alert (quantity ≤ 3)
   - ✅ Expiration alert (within 7 days)
   - ✅ Update item details
   - ✅ Delete items
   - ✅ Increase item quantity
   - ✅ Decrease item quantity
   - ✅ Prevent negative quantity after decrease
   - ✅ Image thumbnail generation

**Run:**
```bash
python manage.py test accounts.tests.test_backend.ItemManagementTests
```

### 4. **Settings and API Tests** (7 tests)
   - ✅ Settings page accessibility
   - ✅ Change email successfully
   - ✅ Prevent duplicate email change
   - ✅ Change password successfully
   - ✅ Password change validation (old password verification)
   - ✅ Password confirmation requirement
   - ✅ Password strength validation

**Run:**
```bash
python manage.py test accounts.tests.test_backend.SettingsAndAPITests
```

### 5. **Access Control Tests** (3 tests)
   - ✅ Prevent cross-user inventory access
   - ✅ Prevent cross-user item modification
   - ✅ Prevent cross-user inventory deletion

**Run:**
```bash
python manage.py test accounts.tests.test_backend.AccessControlTests
```

---

## Frontend Tests (`test_frontend.py`)

Comprehensive frontend testing with 50+ test cases covering:

### 1. **Form Validation Tests** (5 tests)
   - ✅ Registration form rendering
   - ✅ Registration form required fields
   - ✅ Login form rendering
   - ✅ Login form required fields
   - ✅ Item form rendering
   - ✅ Settings form rendering

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.FormValidationTests
```

### 2. **Template Rendering Tests** (9 tests)
   - ✅ Dashboard displays user info
   - ✅ Dashboard displays user's inventories
   - ✅ Inventory items page displays items
   - ✅ Image thumbnail displays
   - ✅ Low stock badge displays (quantity ≤ 3)
   - ✅ Expiration date displays
   - ✅ Navbar displays for authenticated users
   - ✅ Logout link in navbar
   - ✅ Login redirect for authenticated users

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.TemplateRenderingTests
```

### 3. **Pagination Tests** (2 tests)
   - ✅ Pagination displays with 10+ items
   - ✅ Pagination navigation works correctly

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.PaginationTests
```

### 4. **Sorting and Filtering Tests** (6 tests)
   - ✅ Sort by quantity ascending
   - ✅ Sort by quantity descending
   - ✅ Sort by name ascending
   - ✅ Sort by name descending
   - ✅ Search items by name
   - ✅ Search items by brand

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.SortingAndFilteringTests
```

### 5. **Responsive Design Tests** (4 tests)
   - ✅ Bootstrap classes present
   - ✅ Mobile menu elements exist
   - ✅ Form inputs are responsive
   - ✅ Tables are responsive

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.ResponsiveDesignTests
```

### 6. **JavaScript Functionality Tests** (6 tests)
   - ✅ Quantity update AJAX endpoint
   - ✅ Create inventory AJAX endpoint
   - ✅ Delete item AJAX returns JSON
   - ✅ Search functionality via GET
   - ✅ Sorting via GET request

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.JavaScriptFunctionalityTests
```

### 7. **User Interface Elements Tests** (7 tests)
   - ✅ Buttons have Bootstrap classes
   - ✅ Error alerts display
   - ✅ Form labels present
   - ✅ Empty state messages
   - ✅ Emojis display in inventories
   - ✅ Navbar has user menu
   - ✅ Footer present

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.UserInterfaceElementsTests
```

### 8. **Item Image Upload Tests** (6 tests)
   - ✅ Image upload creates file
   - ✅ Thumbnail generation
   - ✅ Inventory items page displays thumbnails
   - ✅ Non-image files handling
   - ✅ Large image files accepted

**Run:**
```bash
python manage.py test accounts.tests.test_frontend.ItemImageUploadTests
```

---

## Running Tests with Coverage

### Install Coverage Tool
```bash
pip install coverage
```

### Run Tests with Coverage Report
```bash
coverage run --source='accounts' manage.py test accounts.tests
coverage report
```

### Generate HTML Coverage Report
```bash
coverage html
# Open htmlcov/index.html in browser
```

---

## Running Tests in Docker

### Build and Run Tests
```bash
docker build -t inventory-app .
docker run --rm -w /app inventory-app python manage.py test accounts.tests
```

### Run Specific Test Suite in Docker
```bash
docker run --rm -w /app inventory-app python manage.py test accounts.tests.test_backend
docker run --rm -w /app inventory-app python manage.py test accounts.tests.test_frontend
```

---

## Running Tests with Verbose Output

### Verbosity Level 0 (Minimal)
```bash
python manage.py test accounts.tests --verbosity=0
```

### Verbosity Level 1 (Normal - Default)
```bash
python manage.py test accounts.tests --verbosity=1
```

### Verbosity Level 2 (Verbose)
```bash
python manage.py test accounts.tests --verbosity=2
```

### Verbosity Level 3 (Very Verbose)
```bash
python manage.py test accounts.tests --verbosity=3
```

---

## Cloud Build CI/CD Integration

### Setup CI/CD Pipeline

1. **Connect GitHub Repository**
   ```bash
   # In Cloud Console:
   # 1. Go to Cloud Build > Triggers
   # 2. Click "Connect Repository"
   # 3. Select GitHub account and inventory_app repository
   # 4. Click "Connect"
   ```

2. **Create Build Trigger**
   ```bash
   # In Cloud Console:
   # 1. Click "Create Trigger"
   # 2. Name: "Inventory App CI/CD"
   # 3. Event: Push to branch
   # 4. Branch: ^main$
   # 5. Build configuration: Cloud Build configuration file
   # 6. Cloud Build configuration file location: /cloudbuild-cicd.yaml
   ```

### Build Pipeline Steps

The `cloudbuild-cicd.yaml` file automatically:

1. **Builds Docker image** - Creates container with all dependencies
2. **Runs backend tests** - Executes all backend test suites
3. **Runs frontend tests** - Executes all frontend test suites
4. **Pushes image** - Pushes tested image to Artifact Registry
5. **Deploys to Cloud Run** - Deploys only if all tests pass

### Monitor Build Logs
```bash
# View recent builds
gcloud builds list

# View specific build logs
gcloud builds log BUILD_ID

# Stream build logs in real-time
gcloud builds log BUILD_ID --stream
```

---

## Test Organization

### File Structure
```
accounts/
├── tests/
│   ├── __init__.py
│   ├── test_backend.py      # 60+ backend tests
│   └── test_frontend.py     # 50+ frontend tests
```

### Total Test Coverage
- **110+ automated test cases**
- **Backend**: Authentication, CRUD, API, Validation, Access Control
- **Frontend**: Forms, Templates, UI, Pagination, Sorting, Filtering, Images
- **End-to-end**: Full user workflows from registration to item management

---

## Common Test Commands

### Run All Tests
```bash
python manage.py test accounts.tests
```

### Run All Tests (Verbose)
```bash
python manage.py test accounts.tests --verbosity=2
```

### Run Tests for Specific Feature
```bash
# User authentication
python manage.py test accounts.tests.test_backend.UserAuthenticationTests

# Item management
python manage.py test accounts.tests.test_backend.ItemManagementTests

# Image uploads
python manage.py test accounts.tests.test_frontend.ItemImageUploadTests
```

### Run with Fail-Fast (Stop on first failure)
```bash
python manage.py test accounts.tests --failfast
```

### Run with Keep-Database Flag
```bash
python manage.py test accounts.tests --keepdb
```

### Parallel Test Execution
```bash
# Install django-test-plus for parallel execution
pip install django-test-plus

# Run tests in parallel
python manage.py test accounts.tests --parallel 4
```

---

## Troubleshooting Tests

### Database Errors
```bash
# Reset test database
python manage.py flush

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
```

### Import Errors
```bash
# Ensure accounts app is in INSTALLED_APPS in settings.py
# Run from project root directory
cd /path/to/inventory_app
python manage.py test accounts.tests
```

### Static Files Issues
```bash
# Collect static files
python manage.py collectstatic --noinput
```

### Permissions Issues
```bash
# Fix file permissions
chmod +x manage.py
```

---

## Continuous Testing During Development

### Watch for Changes and Run Tests
```bash
# Install watchdog
pip install watchdog-auto-reload

# Run tests automatically on file changes
python manage.py test accounts.tests --watch
```

### Run Tests on Git Commit
```bash
# Create pre-commit hook to run tests before committing
# Save as .git/hooks/pre-commit

#!/bin/bash
python manage.py test accounts.tests
if [ $? -ne 0 ]; then
  echo "Tests failed. Commit aborted."
  exit 1
fi
```

---

## Expected Test Results

When running all tests:

```
Ran 110 tests in 15.234s

OK
----------------------------------------------------------------------
Ran 110 tests with 0 failures
```

### Backend Test Results (60+ tests)
```
UserAuthenticationTests ..................... ok
InventoryManagementTests .................... ok
ItemManagementTests ......................... ok
SettingsAndAPITests ......................... ok
AccessControlTests .......................... ok
```

### Frontend Test Results (50+ tests)
```
FormValidationTests ......................... ok
TemplateRenderingTests ...................... ok
PaginationTests ............................. ok
SortingAndFilteringTests .................... ok
ResponsiveDesignTests ....................... ok
JavaScriptFunctionalityTests ................ ok
UserInterfaceElementsTests .................. ok
ItemImageUploadTests ........................ ok
```

---

## Next Steps

1. **Run Tests Locally**
   ```bash
   python manage.py test accounts.tests --verbosity=2
   ```

2. **Check Coverage**
   ```bash
   coverage run --source='accounts' manage.py test accounts.tests
   coverage report
   ```

3. **Setup Cloud Build**
   - Follow "Cloud Build CI/CD Integration" section
   - Tests will run automatically on every push to main branch

4. **Monitor Deployments**
   ```bash
   gcloud builds list
   gcloud run services describe inventory-app
   ```

---

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/5.2/topics/testing/)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
