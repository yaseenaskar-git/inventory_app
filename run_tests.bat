@echo off
REM Run CI/CD Tests for Inventory App
REM Usage: run_tests.bat [backend|frontend|all|coverage]

setlocal enabledelayedexpansion

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

if "%1%"=="" (
    echo Running all tests with verbose output...
    python manage.py test accounts.tests --verbosity=2
    goto :end
)

if "%1%"=="backend" (
    echo Running backend tests...
    python manage.py test accounts.tests.test_backend --verbosity=2
    goto :end
)

if "%1%"=="frontend" (
    echo Running frontend tests...
    python manage.py test accounts.tests.test_frontend --verbosity=2
    goto :end
)

if "%1%"=="all" (
    echo Running all tests...
    python manage.py test accounts.tests --verbosity=2
    goto :end
)

if "%1%"=="coverage" (
    echo Running tests with coverage report...
    coverage run --source='accounts' manage.py test accounts.tests
    coverage report
    coverage html
    echo Coverage report generated in htmlcov/index.html
    goto :end
)

if "%1%"=="quick" (
    echo Running quick tests (failfast)...
    python manage.py test accounts.tests --failfast
    goto :end
)

echo.
echo Usage: run_tests.bat [option]
echo.
echo Options:
echo   (no args)    Run all tests with verbose output
echo   backend      Run only backend tests
echo   frontend     Run only frontend tests
echo   all          Run all tests
echo   coverage     Run tests with coverage report
echo   quick        Run tests with failfast
echo.
echo Examples:
echo   run_tests.bat backend
echo   run_tests.bat coverage

:end
endlocal
