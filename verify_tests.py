"""
Test Setup Verification Script
Verifies that all testing files are properly installed and configured
Run: python verify_tests.py
"""

import os
import sys
import json
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        print_success(f"{description} ({filepath}) - {file_size} bytes")
        return True
    else:
        print_error(f"{description} ({filepath}) - NOT FOUND")
        return False

def check_file_contains(filepath, search_string, description):
    """Check if a file contains a specific string"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print_success(f"{description}")
                return True
            else:
                print_error(f"{description} - String not found")
                return False
    except Exception as e:
        print_error(f"Error reading {filepath}: {e}")
        return False

def count_test_cases(filepath):
    """Count number of test methods in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Count def test_ methods
            count = content.count('def test_')
            return count
    except:
        return 0

def main():
    print_header("INVENTORY APP - CI/CD TESTING VERIFICATION")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Track results
    all_checks_passed = True
    
    # 1. Check test files exist
    print_header("1. Checking Test Files")
    
    test_backend = os.path.join(project_root, 'accounts', 'tests', 'test_backend.py')
    test_frontend = os.path.join(project_root, 'accounts', 'tests', 'test_frontend.py')
    test_init = os.path.join(project_root, 'accounts', 'tests', '__init__.py')
    
    if not check_file_exists(test_backend, "Backend test file"):
        all_checks_passed = False
    if not check_file_exists(test_frontend, "Frontend test file"):
        all_checks_passed = False
    if not check_file_exists(test_init, "Test package init file"):
        all_checks_passed = False
    
    # 2. Count test cases
    print_header("2. Counting Test Cases")
    
    backend_tests = count_test_cases(test_backend)
    frontend_tests = count_test_cases(test_frontend)
    total_tests = backend_tests + frontend_tests
    
    print_info(f"Backend test methods: {backend_tests}")
    print_info(f"Frontend test methods: {frontend_tests}")
    print_info(f"Total test methods: {total_tests}")
    
    if total_tests >= 100:
        print_success(f"Found {total_tests} test cases (Expected: 100+)")
    else:
        print_warning(f"Found {total_tests} test cases (Expected: 100+)")
    
    # 3. Check CI/CD configuration
    print_header("3. Checking CI/CD Configuration")
    
    cloudbuild_cicd = os.path.join(project_root, 'cloudbuild-cicd.yaml')
    if check_file_exists(cloudbuild_cicd, "Cloud Build CI/CD config"):
        if check_file_contains(cloudbuild_cicd, 'test_backend', "Cloud Build tests backend"):
            pass
        else:
            all_checks_passed = False
        if check_file_contains(cloudbuild_cicd, 'test_frontend', "Cloud Build tests frontend"):
            pass
        else:
            all_checks_passed = False
    else:
        all_checks_passed = False
    
    # 4. Check documentation
    print_header("4. Checking Documentation")
    
    testing_guide = os.path.join(project_root, 'TESTING_GUIDE.md')
    ci_cd_summary = os.path.join(project_root, 'CI_CD_TESTING_SUMMARY.md')
    
    if check_file_exists(testing_guide, "Comprehensive Testing Guide"):
        check_file_contains(testing_guide, 'Quick Start', "Testing guide has quick start section")
    else:
        all_checks_passed = False
    
    if check_file_exists(ci_cd_summary, "CI/CD Testing Summary"):
        check_file_contains(ci_cd_summary, 'Run Tests on Windows', "Summary has Windows instructions")
    else:
        all_checks_passed = False
    
    # 5. Check test runner scripts
    print_header("5. Checking Test Runner Scripts")
    
    run_tests_bat = os.path.join(project_root, 'run_tests.bat')
    run_tests_sh = os.path.join(project_root, 'run_tests.sh')
    
    if check_file_exists(run_tests_bat, "Windows test runner script"):
        check_file_contains(run_tests_bat, 'test accounts.tests', "Windows script has test command")
    else:
        all_checks_passed = False
    
    if check_file_exists(run_tests_sh, "Linux/Mac test runner script"):
        check_file_contains(run_tests_sh, 'test accounts.tests', "Linux/Mac script has test command")
    else:
        all_checks_passed = False
    
    # 6. Check test coverage
    print_header("6. Test Coverage Analysis")
    
    try:
        with open(test_backend, 'r', encoding='utf-8') as f:
            backend_content = f.read()
            
        # Count test classes
        backend_classes = backend_content.count('class ')
        
        print_info(f"Backend test classes: {backend_classes}")
        
        # Check key test classes
        test_classes = [
            'UserAuthenticationTests',
            'InventoryManagementTests',
            'ItemManagementTests',
            'SettingsAndAPITests',
            'AccessControlTests'
        ]
        
        for test_class in test_classes:
            if test_class in backend_content:
                print_success(f"Found {test_class}")
            else:
                print_warning(f"Missing {test_class}")
    except Exception as e:
        print_error(f"Error analyzing backend tests: {e}")
        all_checks_passed = False
    
    try:
        with open(test_frontend, 'r', encoding='utf-8') as f:
            frontend_content = f.read()
            
        # Count test classes
        frontend_classes = frontend_content.count('class ')
        
        print_info(f"Frontend test classes: {frontend_classes}")
        
        # Check key test classes
        test_classes = [
            'FormValidationTests',
            'TemplateRenderingTests',
            'PaginationTests',
            'SortingAndFilteringTests',
            'ResponsiveDesignTests',
            'JavaScriptFunctionalityTests',
            'UserInterfaceElementsTests',
            'ItemImageUploadTests'
        ]
        
        for test_class in test_classes:
            if test_class in frontend_content:
                print_success(f"Found {test_class}")
            else:
                print_warning(f"Missing {test_class}")
    except Exception as e:
        print_error(f"Error analyzing frontend tests: {e}")
        all_checks_passed = False
    
    # 7. Check Django configuration
    print_header("7. Checking Django Configuration")
    
    settings_file = os.path.join(project_root, 'inventory_app', 'settings.py')
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings_content = f.read()
        
        if "'accounts'" in settings_content or '"accounts"' in settings_content:
            print_success("'accounts' app in INSTALLED_APPS")
        else:
            print_warning("'accounts' app may not be in INSTALLED_APPS")
    except Exception as e:
        print_error(f"Error reading settings.py: {e}")
    
    # 8. Final summary
    print_header("VERIFICATION SUMMARY")
    
    if all_checks_passed and total_tests >= 100:
        print_success("✅ All verification checks PASSED!")
        print_success(f"✅ Found {total_tests} test cases")
        print_success("✅ Testing infrastructure is ready!")
        print_info("\nNext steps:")
        print_info("1. Run tests locally: python manage.py test accounts.tests --verbosity=2")
        print_info("2. Or use: run_tests.bat (Windows) or ./run_tests.sh (Linux/Mac)")
        print_info("3. Setup Cloud Build trigger for automated testing on push")
        return 0
    else:
        print_error("⚠️  Some verification checks did not pass")
        print_error("Please review the errors above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
