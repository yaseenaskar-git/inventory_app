#!/bin/bash
# Run CI/CD Tests for Inventory App
# Usage: ./run_tests.sh [backend|frontend|all|coverage|quick]

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

# Default to all tests if no argument provided
OPTION="${1:-all}"

case $OPTION in
    backend)
        print_status "Running backend tests..."
        python manage.py test accounts.tests.test_backend --verbosity=2
        ;;
    frontend)
        print_status "Running frontend tests..."
        python manage.py test accounts.tests.test_frontend --verbosity=2
        ;;
    all)
        print_status "Running all tests..."
        python manage.py test accounts.tests --verbosity=2
        ;;
    coverage)
        print_status "Running tests with coverage report..."
        coverage run --source='accounts' manage.py test accounts.tests
        coverage report
        coverage html
        print_status "Coverage report generated in htmlcov/index.html"
        ;;
    quick)
        print_status "Running quick tests (failfast)..."
        python manage.py test accounts.tests --failfast
        ;;
    *)
        echo ""
        echo "Usage: $0 [option]"
        echo ""
        echo "Options:"
        echo "  (no args)    Run all tests with verbose output"
        echo "  backend      Run only backend tests"
        echo "  frontend     Run only frontend tests"
        echo "  all          Run all tests"
        echo "  coverage     Run tests with coverage report"
        echo "  quick        Run tests with failfast"
        echo ""
        echo "Examples:"
        echo "  $0 backend"
        echo "  $0 coverage"
        echo "  $0 quick"
        echo ""
        ;;
esac
