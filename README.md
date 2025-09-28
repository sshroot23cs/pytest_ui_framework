# UI Automation Framework

## Overview
This is a comprehensive UI automation framework built with pytest and Selenium, designed for end-to-end testing of web applications. The framework uses a page object model architecture and supports advanced features like Allure reporting, parallel execution, and screenshot capture on failures.

## Features
- 🎯 **Page Object Model**: Clean, maintainable test structure
- 📊 **Allure Reporting**: Beautiful test reports with detailed insights
- 🔄 **Parallel Execution**: Run tests in parallel with pytest-xdist
- 📸 **Screenshot on Failure**: Automatic screenshot capture for failed tests
- 🌐 **Multi-browser Support**: Chrome and Firefox support
- 📝 **YAML Locators**: Externalized locator management
- 🧪 **End-to-End Testing**: Comprehensive E2E test scenarios

## Project Structure
```
pytest_ui_framework/
├── src/                          # Source code
│   ├── __init__.py
│   ├── common_page_elements.py   # Base page elements and utilities
│   ├── helper.py                 # Helper functions
│   ├── pages.py                  # Page object manager
│   ├── search.py                 # Search page specific methods
│   └── locators/
│       └── search_locators.yaml  # Page locators in YAML format
├── tests/                        # Test files
│   ├── conftest.py              # pytest configuration and fixtures
│   ├── test_sample_01.py        # Sample test
│   └── test_e2e_search.py       # End-to-end search tests
├── reports/                      # Test reports and artifacts
├── assets/                       # Static assets (CSS, etc.)
├── requirements.txt              # Python dependencies
├── pytest.ini                   # pytest configuration
├── setup.cfg                     # Setup configuration
├── tox.ini                       # Tox configuration
└── validate_framework.py         # Framework validation script
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pytest_ui_framework
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install WebDriver**
   Make sure you have Chrome or Firefox WebDriver installed and in your PATH.

## Usage

### Running Tests

**Run all tests:**
```bash
python -m pytest
```

**Run specific test file:**
```bash
python -m pytest tests/test_e2e_search.py
```

**Run with verbose output:**
```bash
python -m pytest tests/test_e2e_search.py -v
```

**Run with specific browser:**
```bash
python -m pytest --browser=firefox
```

**Run in parallel:**
```bash
python -m pytest -n auto
```

### Running E2E Tests

The framework includes comprehensive end-to-end tests for search functionality:

```bash
# Run all E2E search tests
python -m pytest tests/test_e2e_search.py -v

# Run specific E2E test
python -m pytest tests/test_e2e_search.py::TestE2ESearch::test_e2e_search_stock_symbol -v

# Run with allure reporting
python -m pytest tests/test_e2e_search.py --alluredir=reports/allure-results
```

### Test Scenarios

#### E2E Search Tests (`test_e2e_search.py`)

1. **Stock Symbol Search Test** - Tests complete search workflow for stock symbols
2. **Multiple Stocks Test** - Tests searching for multiple different stock symbols
3. **Error Handling Test** - Tests search functionality with invalid inputs
4. **Performance Test** - Tests search response times and performance

### Allure Reporting

**Generate and view Allure reports:**
```bash
# Run tests with allure
python -m pytest --alluredir=reports/allure-results

# Generate and serve report (requires allure command-line tool)
allure serve reports/allure-results
```

### Framework Validation

**Validate framework setup:**
```bash
python validate_framework.py
```

This script checks:
- All required modules can be imported
- Test file structure is correct
- Locator files exist
- Framework is ready for testing

## Configuration

### pytest.ini
Main pytest configuration file with settings for:
- Test discovery patterns
- Allure integration
- HTML reporting
- JUnit XML output

### Browser Configuration
Configure browser through command line:
```bash
python -m pytest --browser=chrome  # Default
python -m pytest --browser=firefox
```

### Locators Management
Locators are stored in YAML files under `src/locators/`:

```yaml
# Example: search_locators.yaml
search-box:
  type: "xpath"
  value: "//input[@placeholder='Search']"

search-button:
  type: "css"
  value: "button[type='submit']"
```

## Page Object Model

### Base Classes
- **CommonPageElements**: Base class with common web element operations
- **Helper**: Utility functions for loading locators and common operations

### Page Classes
- **SearchPage**: Handles all search-related operations
- **Pages**: Main page object manager

### Example Usage
```python
def test_search_functionality(browser, get_pages_object):
    # Navigate to page
    browser.get("https://www.google.com/finance/")
    
    # Use page object methods
    search_element = get_pages_object.search.check_search_element()
    assert search_element, "Search box not found"
    
    # Perform search
    result = get_pages_object.search.search_for_stock("AAPL")
    assert result, "Search failed"
```

## Dependencies

Core dependencies:
- **pytest**: Testing framework
- **selenium**: Web automation
- **allure-pytest**: Reporting
- **pyyaml**: YAML file handling
- **pytest-xdist**: Parallel execution
- **pytest-failed-screenshot**: Screenshot on failure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
