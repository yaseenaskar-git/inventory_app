# QUICK START: Running Your Tests

This is a quick reference for running your automated tests. For detailed information, see `TESTING_GUIDE.md`.

---

## ⚡ FASTEST WAY TO GET STARTED

### Step 1: Open PowerShell/Terminal
```powershell
# Open PowerShell and navigate to your project
cd c:\Users\yasee\inventory_app
```

### Step 2: Verify Setup
```powershell
# Check that all testing files are installed correctly
python verify_tests.py
```

You should see:
```
✅ Backend test file (...\accounts\tests\test_backend.py) - XXXXX bytes
✅ Frontend test file (...\accounts\tests\test_frontend.py) - XXXXX bytes
✅ Found 110+ test cases
✅ Testing infrastructure is ready!
```

### Step 3: Run Tests
```powershell
# Option 1: Windows batch script (EASIEST)
run_tests.bat

# Option 2: Direct Django command
python manage.py test accounts.tests --verbosity=2
```

That's it! ✅

---

## 🎯 COMMON TEST COMMANDS

### Run All Tests (Verbose Output)
```powershell
python manage.py test accounts.tests --verbosity=2
```

### Run Only Backend Tests
```powershell
python manage.py test accounts.tests.test_backend --verbosity=2
```

### Run Only Frontend Tests
```powershell
python manage.py test accounts.tests.test_frontend --verbosity=2
```

### Run Tests (Stop on First Failure)
```powershell
python manage.py test accounts.tests --failfast
```

### Run Tests with Coverage Report
```powershell
coverage run --source='accounts' manage.py test accounts.tests
coverage report
coverage html
# Then open htmlcov/index.html in your browser
```

### Run Specific Test Class
```powershell
python manage.py test accounts.tests.test_backend.UserAuthenticationTests --verbosity=2
```

### Run Single Test Method
```powershell
python manage.py test accounts.tests.test_backend.UserAuthenticationTests.test_user_registration_valid_data
```

---

## 📊 WHAT TO EXPECT

### Successful Test Run
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................................................
----------------------------------------------------------------------
Ran 110 tests in 15.234s

OK
```

### Test Run with Failures
```
FAILED (failures=2, errors=1)
```
(Check the detailed error messages above this line to fix issues)

---

## 🪟 WINDOWS BATCH SCRIPT (EASIEST)

```powershell
# Run all tests (default)
run_tests.bat

# Run backend tests only
run_tests.bat backend

# Run frontend tests only
run_tests.bat frontend

# Run with coverage report
run_tests.bat coverage

# Run with failfast
run_tests.bat quick
```

---

## 🐧 LINUX/MAC BASH SCRIPT

```bash
# Make script executable (first time only)
chmod +x run_tests.sh

# Run all tests (default)
./run_tests.sh

# Run backend tests only
./run_tests.sh backend

# Run frontend tests only
./run_tests.sh frontend

# Run with coverage report
./run_tests.sh coverage

# Run with failfast
./run_tests.sh quick
```

---

## 🐳 RUNNING TESTS IN DOCKER

### Build Docker Image
```powershell
docker build -t inventory-app .
```

### Run All Tests in Docker
```powershell
docker run --rm -w /app inventory-app python manage.py test accounts.tests --verbosity=2
```

### Run Backend Tests in Docker
```powershell
docker run --rm -w /app inventory-app python manage.py test accounts.tests.test_backend --verbosity=2
```

### Run Frontend Tests in Docker
```powershell
docker run --rm -w /app inventory-app python manage.py test accounts.tests.test_frontend --verbosity=2
```

---

## 📈 GENERATE COVERAGE REPORT

```powershell
# Install coverage (if not already installed)
pip install coverage

# Run tests with coverage
coverage run --source='accounts' manage.py test accounts.tests

# View report in terminal
coverage report

# Generate HTML report
coverage html

# Open HTML report in browser
start htmlcov\index.html
```

---

## ☁️ GOOGLE CLOUD BUILD (AUTOMATED)

### Setup (One-time)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Cloud Build > Triggers**
3. Click **Create Trigger**
4. Configure:
   - Name: `Inventory App CI/CD`
   - Event: Push to branch
   - Branch: `^main$`
   - Build config: `cloudbuild-cicd.yaml`
5. Save trigger

### After Setup (Automatic)
- Every time you push to `main` branch:
  1. Tests automatically run
  2. If all tests pass → Image pushed to registry
  3. If all tests pass → Deployed to Cloud Run

### View Build Status
```powershell
# List all builds
gcloud builds list

# View specific build logs
gcloud builds log BUILD_ID --stream

# View latest build
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)') --stream
```

---

## 🔧 TROUBLESHOOTING

### Issue: "ModuleNotFoundError: No module named 'accounts'"
**Solution:**
```powershell
# Make sure you're in the project root
cd c:\Users\yasee\inventory_app

# Run tests
python manage.py test accounts.tests
```

### Issue: "Database does not exist"
**Solution:**
```powershell
# Run migrations
python manage.py migrate

# Then run tests
python manage.py test accounts.tests
```

### Issue: "No such table: accounts_inventory"
**Solution:**
```powershell
# Reset database
python manage.py flush --noinput

# Run migrations
python manage.py migrate

# Run tests
python manage.py test accounts.tests
```

### Issue: "Connection refused" (Tests fail trying to connect)
**Solution:**
```powershell
# Kill any running Django instances
# Look for processes on port 8000 and kill them

# Then run tests
python manage.py test accounts.tests --verbosity=2
```

### Issue: "Permission denied" (Linux/Mac)
**Solution:**
```bash
# Make scripts executable
chmod +x run_tests.sh
chmod +x manage.py

# Then run tests
./run_tests.sh
```

---

## 📝 TEST STRUCTURE

### Backend Tests (60+ tests)
```
test_backend.py
├── UserAuthenticationTests (12 tests)
│   ├── Registration validation
│   ├── Password validation
│   ├── Login/Logout
│   └── Authentication checks
├── InventoryManagementTests (7 tests)
│   ├── CRUD operations
│   └── User isolation
├── ItemManagementTests (15 tests)
│   ├── Item CRUD
│   ├── Quantity tracking
│   └── Image uploads
├── SettingsAndAPITests (7 tests)
│   ├── Email/Password changes
│   └── API endpoints
└── AccessControlTests (3 tests)
    └── Cross-user access prevention
```

### Frontend Tests (50+ tests)
```
test_frontend.py
├── FormValidationTests (5 tests)
│   └── Form rendering & fields
├── TemplateRenderingTests (9 tests)
│   └── UI display & content
├── PaginationTests (2 tests)
│   └── Pagination functionality
├── SortingAndFilteringTests (6 tests)
│   ├── Sorting
│   └── Searching
├── ResponsiveDesignTests (4 tests)
│   └── Bootstrap & mobile
├── JavaScriptFunctionalityTests (6 tests)
│   └── AJAX & user interactions
├── UserInterfaceElementsTests (7 tests)
│   └── UI components
└── ItemImageUploadTests (6 tests)
    └── Image handling
```

---

## 🎓 WHAT GETS TESTED

### Authentication ✅
- User registration with password validation
- Login/logout functionality
- Account security

### Data Management ✅
- Inventory CRUD operations
- Item management (create, read, update, delete)
- Quantity tracking
- Image uploads & thumbnails

### User Experience ✅
- Form validation
- Template rendering
- Sorting & filtering
- Pagination
- Responsive design

### Access Control ✅
- User data isolation
- Permission checking
- Cross-user access prevention

### API Endpoints ✅
- JSON responses
- AJAX functionality
- Error handling

---

## 🚀 NEXT STEPS

### 1. Verify Everything Works
```powershell
python verify_tests.py
```

### 2. Run Tests Locally
```powershell
run_tests.bat
```

### 3. Check Coverage
```powershell
run_tests.bat coverage
```

### 4. Setup Cloud Build (Optional)
See "☁️ GOOGLE CLOUD BUILD" section above

### 5. Push to GitHub
```powershell
git add accounts/tests/ *.bat *.sh *.yaml *.md *.py
git commit -m "Add automated CI/CD testing with 110+ tests"
git push origin main
```

---

## 📚 For More Information

- **Full Testing Guide:** See `TESTING_GUIDE.md`
- **CI/CD Summary:** See `CI_CD_TESTING_SUMMARY.md`
- **Verification:** Run `python verify_tests.py`
- **Django Testing Docs:** https://docs.djangoproject.com/en/5.2/topics/testing/

---

## ✨ SUMMARY

You have:
- ✅ 110+ comprehensive test cases
- ✅ Windows batch script for easy running
- ✅ Linux/Mac bash script for easy running
- ✅ Google Cloud Build CI/CD setup
- ✅ Coverage report generation
- ✅ Complete documentation

**To run tests NOW:**
```powershell
run_tests.bat
```

**Done!** 🎉
