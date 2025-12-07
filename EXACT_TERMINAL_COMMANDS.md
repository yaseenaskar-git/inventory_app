# STEP-BY-STEP: RUN YOUR TESTS NOW

This file shows you the EXACT commands to type in PowerShell to run your tests.

---

## ✅ STEP 1: OPEN POWERSHELL

1. Press `Win + R`
2. Type `powershell`
3. Press `Enter`

Or search for "PowerShell" in Windows Start menu

---

## ✅ STEP 2: GO TO YOUR PROJECT

Copy and paste this into PowerShell:

```powershell
cd c:\Users\yasee\inventory_app
```

Press `Enter`

**You should see:** `C:\Users\yasee\inventory_app>`

---

## ✅ STEP 3: VERIFY TESTS ARE INSTALLED

Copy and paste this into PowerShell:

```powershell
python verify_tests.py
```

Press `Enter`

**You should see:**
```
✅ Backend test file (...\accounts\tests\test_backend.py)
✅ Frontend test file (...\accounts\tests\test_frontend.py)
✅ Found 110+ test cases
✅ Testing infrastructure is ready!
```

If you see this, go to Step 4. If not, something went wrong - see Troubleshooting section.

---

## ✅ STEP 4: RUN YOUR TESTS

### **Option A: Easy Way (RECOMMENDED)**

Copy and paste this into PowerShell:

```powershell
run_tests.bat
```

Press `Enter`

**This will run ALL tests with nice formatting.**

---

### **Option B: Direct Django Command**

Copy and paste this into PowerShell:

```powershell
python manage.py test accounts.tests --verbosity=2
```

Press `Enter`

**This runs the exact same tests as Option A.**

---

### **Option C: Specific Tests**

**Run only backend tests:**
```powershell
python manage.py test accounts.tests.test_backend --verbosity=2
```

**Run only frontend tests:**
```powershell
python manage.py test accounts.tests.test_frontend --verbosity=2
```

**Run with stop-on-error (faster):**
```powershell
python manage.py test accounts.tests --failfast
```

---

## 📊 WHAT YOU'LL SEE

While tests run, you'll see dots (periods) appearing:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................................................
----------------------------------------------------------------------
Ran 110 tests in 15.234s

OK
```

**This means:** ✅ ALL TESTS PASSED!

Each dot (.) = 1 passing test
Each F = 1 failing test (red text)
Each E = 1 error (red text)

---

## ✅ SUCCESS INDICATORS

### **Perfect Output** ✅
```
Ran 110 tests in 15.234s
OK
```

### **One or More Failed** ❌
```
FAILED (failures=2, errors=1)
```

If you see failures, read the error message above them to see what went wrong.

---

## 📈 GENERATE COVERAGE REPORT

After running tests, you can see code coverage:

Copy and paste this into PowerShell:

```powershell
coverage run --source='accounts' manage.py test accounts.tests
```

Then:

```powershell
coverage report
```

You'll see something like:
```
Name                        Stmts   Miss  Cover
----------------------------------------------
accounts/__init__.py            0      0   100%
accounts/admin.py              15      2    87%
accounts/forms.py              45      5    89%
accounts/models.py             50      3    94%
accounts/urls.py              12      0   100%
accounts/views.py             180     15    92%
----------------------------------------------
TOTAL                         302     25    92%
```

This shows how many lines of code are being tested. Higher is better. Aim for 80%+.

---

## 🧪 OTHER USEFUL COMMANDS

### **Run Just Backend Tests**
```powershell
run_tests.bat backend
```

### **Run Just Frontend Tests**
```powershell
run_tests.bat frontend
```

### **Run With Coverage Report**
```powershell
run_tests.bat coverage
```

Then open `htmlcov\index.html` in your browser for a visual report.

### **Run Tests That Stop on First Error**
```powershell
run_tests.bat quick
```

This is faster if you just want to see what fails first.

### **Verify Your Setup**
```powershell
python verify_tests.py
```

Run this anytime to check that all test files are installed correctly.

---

## 🐳 RUNNING TESTS IN DOCKER

If you have Docker installed and running:

### **Build Docker Image**
```powershell
docker build -t inventory-app .
```

### **Run Tests in Docker**
```powershell
docker run --rm -w /app inventory-app python manage.py test accounts.tests --verbosity=2
```

---

## ⚡ QUICK REFERENCE

| What You Want | Command |
|---|---|
| Run all tests | `run_tests.bat` |
| Run backend only | `run_tests.bat backend` |
| Run frontend only | `run_tests.bat frontend` |
| Run with coverage | `run_tests.bat coverage` |
| Run quick (stop on error) | `run_tests.bat quick` |
| Verify setup | `python verify_tests.py` |
| Direct Django command | `python manage.py test accounts.tests --verbosity=2` |
| Coverage report | `coverage run --source='accounts' manage.py test accounts.tests` |
| View coverage | `coverage report` |
| HTML coverage | `coverage html` then open `htmlcov\index.html` |

---

## 🔧 TROUBLESHOOTING

### **PowerShell says "run_tests.bat: The term 'run_tests.bat' is not recognized"**

**Solution:** You're in the wrong directory. Do this:

```powershell
cd c:\Users\yasee\inventory_app
run_tests.bat
```

### **Tests say "ModuleNotFoundError: No module named 'accounts'"**

**Solution:** You're in wrong directory or Django isn't installed:

```powershell
# Make sure you're here
cd c:\Users\yasee\inventory_app

# Install Django if needed
pip install django

# Run tests
run_tests.bat
```

### **Tests fail with "Database does not exist"**

**Solution:** Run migrations first:

```powershell
python manage.py migrate
python manage.py test accounts.tests --verbosity=2
```

### **Nothing shows when I type run_tests.bat**

**Solution:** The script might not be executable. Try the direct command instead:

```powershell
python manage.py test accounts.tests --verbosity=2
```

### **"Permission denied" or similar error**

**Solution:** Make sure Python is installed and in your PATH:

```powershell
python --version
```

If this doesn't work, Python isn't installed or not in your PATH.

---

## 📝 STEP-BY-STEP SUMMARY

1. **Open PowerShell** - Press Win+R, type "powershell"
2. **Go to project** - Paste: `cd c:\Users\yasee\inventory_app`
3. **Verify tests exist** - Paste: `python verify_tests.py`
4. **Run tests** - Paste: `run_tests.bat`
5. **See results** - Wait 15 seconds for "OK" message
6. **Check coverage** - Paste: `run_tests.bat coverage`

---

## ✨ THAT'S IT!

You should now see:

```
Ran 110 tests in 15.234s
OK
```

This means all your tests are passing! 🎉

---

## 📚 NEXT READING

- For more info: **RUN_TESTS_QUICK_START.md**
- For detailed guide: **TESTING_GUIDE.md**
- For implementation: **CI_CD_TESTING_SUMMARY.md**

---

## 🎯 COMMON NEXT STEPS

### **After tests pass locally:**
1. Generate coverage report: `run_tests.bat coverage`
2. Commit changes: `git add .` then `git commit -m "Add tests"`
3. Push to GitHub: `git push origin main`
4. Watch Cloud Build automatically run tests in cloud

### **To add new tests:**
1. Open `accounts/tests/test_backend.py` or `test_frontend.py`
2. Add new test methods following existing patterns
3. Run tests: `run_tests.bat`

### **To see Cloud Build results:**
1. Go to https://console.cloud.google.com/cloud-build/builds
2. Or run in PowerShell: `gcloud builds list`

---

## 🚀 RUN TESTS RIGHT NOW

**Copy and paste into PowerShell:**

```powershell
cd c:\Users\yasee\inventory_app && run_tests.bat
```

That's ONE command. Copy it, paste it into PowerShell, press Enter.

Done! ✅

---

## ❓ QUESTIONS?

- Test not running? → See Troubleshooting section above
- Want more tests? → See TESTING_GUIDE.md
- Need coverage report? → Run `run_tests.bat coverage`
- Want Cloud Build? → See CI_CD_TESTING_SUMMARY.md

**Happy testing!** 🎉
