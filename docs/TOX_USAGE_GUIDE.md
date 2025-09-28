# 🧪 Tox Test Execution Guide

This guide shows how to use tox for running tests in the pytest UI automation framework.

## 🚀 Quick Start Commands

### **Basic Test Execution**
```bash
# Run tests with Chrome browser
tox -e py312-chrome

# Run tests with Firefox browser  
tox -e py312-firefox

# Run tests in headless mode (Chrome)
tox -e py312-headless-chrome

# Run tests in headless mode (Firefox)
tox -e py312-headless-firefox
```

### **Advanced Test Execution**
```bash
# Run tests in parallel
tox -e py312-parallel

# Run full E2E test suite (multi-browser)
tox -e py312-e2e-full

# Validate framework setup
tox -e validate-framework
```

### **Code Quality & Formatting**
```bash
# Run linting checks
tox -e lint

# Check code formatting
tox -e format-check

# Format code automatically
tox -e format
```

### **Report Generation**
```bash
# Generate Allure reports
tox -e allure-report

# Generate and serve Allure reports
tox -e allure-serve
```

### **Utility Commands**
```bash
# Clean all generated files
tox -e clean

# Install browser drivers (for CI/CD)
tox -e install-browsers
```

## 📋 Available Environments

| Environment | Purpose | Browser | Mode | Output |
|-------------|---------|---------|------|--------|
| `py312-chrome` | Chrome testing | Chrome | Windowed | Allure + HTML + JUnit |
| `py312-firefox` | Firefox testing | Firefox | Windowed | Allure + HTML + JUnit |
| `py312-headless-chrome` | Headless Chrome | Chrome | Headless | Allure + HTML + JUnit |
| `py312-headless-firefox` | Headless Firefox | Firefox | Headless | Allure + HTML + JUnit |
| `py312-parallel` | Parallel execution | Chrome | Headless | Allure + HTML + JUnit |
| `py312-e2e-full` | Multi-browser suite | Both | Headless | Combined reports |
| `lint` | Code quality | N/A | N/A | Flake8 output |
| `format-check` | Format validation | N/A | N/A | Black/isort diff |
| `format` | Auto-formatting | N/A | N/A | Formatted files |
| `allure-report` | Report generation | N/A | N/A | HTML reports |
| `validate-framework` | Framework check | N/A | N/A | Validation output |

## 🎯 Usage Examples

### **Development Workflow**
```bash
# 1. Validate framework
tox -e validate-framework

# 2. Check code quality
tox -e lint
tox -e format-check

# 3. Run tests locally
tox -e py312-chrome

# 4. Generate reports
tox -e allure-report
```

### **CI/CD Workflow**
```bash
# 1. Install browsers
tox -e install-browsers

# 2. Run full test suite
tox -e py312-e2e-full

# 3. Check code quality
tox -e lint -e format-check

# 4. Generate reports
tox -e allure-report
```

### **Quick Testing**
```bash
# Fast headless testing
tox -e py312-headless-chrome

# Parallel execution for speed
tox -e py312-parallel
```

## 📊 Report Locations

After running tests, reports will be generated in:

```
reports/
├── allure-results-{env}/     # Raw Allure data
├── allure-report/            # Generated HTML reports  
├── html-report-{env}.html    # Self-contained HTML reports
└── junit-{env}.xml          # JUnit XML reports
```

## ⚙️ Configuration

### **Environment Variables**
- `BROWSER`: chrome | firefox
- `HEADLESS`: true | false  
- `PYTHONPATH`: Automatically set to project root

### **Dependencies**
All environments automatically install:
- pytest and plugins
- selenium
- allure-pytest
- Code quality tools (flake8, black, isort)

## 🔧 Customization

### **Adding New Environments**
```ini
[testenv:my-custom-env]
description = My custom test environment
setenv = 
    {[testenv]setenv}
    CUSTOM_VAR = value
    
commands = 
    python -m pytest tests/ -v --custom-args
```

### **Modifying Existing Environments**
Edit the `tox.ini` file and modify the `commands` section for any environment.

## 🚀 Integration with IDEs

### **VS Code**
Add to `.vscode/tasks.json`:
```json
{
    "label": "Run E2E Tests (Tox)",
    "type": "shell", 
    "command": "tox",
    "args": ["-e", "py312-chrome"],
    "group": "test"
}
```

### **PyCharm**
Create run configuration:
- **Program**: `tox`
- **Arguments**: `-e py312-chrome`
- **Working directory**: Project root

## 📈 Performance Tips

1. **Use headless mode** for faster execution:
   ```bash
   tox -e py312-headless-chrome
   ```

2. **Run tests in parallel** when possible:
   ```bash
   tox -e py312-parallel
   ```

3. **Use specific environments** instead of running all:
   ```bash
   # Instead of: tox
   # Use: tox -e py312-chrome
   ```

4. **Clean old results** regularly:
   ```bash
   tox -e clean
   ```

## 🔍 Troubleshooting

### **Common Issues**
- **Browser not found**: Run `tox -e install-browsers`
- **Permission errors**: Check file permissions in reports directory
- **Import errors**: Run `tox -e validate-framework`
- **Locator failures**: Update locators in `src/locators/` if website structure changes
- **Element not found**: Check if website UI has changed and update YAML locators

### **Debug Mode**
```bash
# Run with verbose output
tox -v -e py312-chrome

# See all tox environments
tox -l

# Check tox installation status
tox --version
```

### **Locator Updates**
If tests fail due to element location issues:
1. Inspect the target website manually
2. Update locators in `src/locators/search_locators.yaml`
3. Test with a single environment: `tox -e py312-chrome`
4. Re-run full suite once locators are fixed

---

*This guide covers the most common tox usage patterns. For advanced configuration, refer to the `tox.ini` file directly.*