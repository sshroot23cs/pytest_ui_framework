#!/usr/bin/env python3
"""
Validation script for the E2E test framework
This script validates that all components are properly set up
"""

import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def validate_imports():
    """Validate that all required modules can be imported"""
    try:
        import pytest
        print("✓ pytest imported successfully")
        
        import selenium
        print("✓ selenium imported successfully")
        
        import allure
        print("✓ allure imported successfully")
        
        from src.pages import Pages
        print("✓ Pages class imported successfully")
        
        from src.search import SearchPage
        print("✓ SearchPage class imported successfully")
        
        from src.common_page_elements import CommonPageElements
        print("✓ CommonPageElements class imported successfully")
        
        from src.helper import Helper
        print("✓ Helper class imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def validate_test_structure():
    """Validate test file structure"""
    test_file = os.path.join('tests', 'test_e2e_search.py')
    if os.path.exists(test_file):
        print("✓ E2E test file exists")
        return True
    else:
        print("✗ E2E test file missing")
        return False

def validate_locators():
    """Validate locators file"""
    locator_file = os.path.join('src', 'locators', 'search_locators.yaml')
    if os.path.exists(locator_file):
        print("✓ Search locators file exists")
        return True
    else:
        print("✗ Search locators file missing")
        return False

def main():
    """Main validation function"""
    print("🔍 Validating E2E Test Framework Setup")
    print("=" * 50)
    
    all_valid = True
    
    print("\n📦 Checking Imports:")
    all_valid &= validate_imports()
    
    print("\n📁 Checking File Structure:")
    all_valid &= validate_test_structure()
    all_valid &= validate_locators()
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All validations passed! Framework is ready for testing.")
        print("\nTo run the E2E tests:")
        print("python -m pytest tests/test_e2e_search.py -v")
        print("\nTo run with allure reporting:")
        print("python -m pytest tests/test_e2e_search.py --alluredir=reports/allure-results")
    else:
        print("❌ Some validations failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())