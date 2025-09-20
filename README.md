# UI Automation Framework

## Overview
This is a comprehensive UI automation framework built with pytest and Selenium, designed for end-to-end testing of web applications. The framework uses a page object model architecture and supports both local development and containerized execution with Docker. It features advanced reporting, monitoring, and cloud deployment capabilities.

## Features
- 🎯 **Page Object Model**: Clean, maintainable test structure
- 📊 **Allure Reporting**: Beautiful test reports with detailed insights
- 🔄 **Parallel Execution**: Run tests in parallel with pytest-xdist
- 📸 **Screenshot on Failure**: Automatic screenshot capture for failed tests
- 🌐 **Multi-browser Support**: Chrome and Firefox support
- 📝 **YAML Locators**: Externalized locator management
- 🧪 **End-to-End Testing**: Comprehensive E2E test scenarios
- 🐳 **Docker Support**: Complete containerized testing environment
- 📈 **Monitoring**: Grafana dashboards and Prometheus metrics
- ☁️ **Cloud Deployment**: Azure Container Instances support
- 🎛️ **Selenium Grid**: Distributed browser testing

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
├── docs/                         # Documentation
│   ├── LOCAL_DOCKER_SETUP.md    # Local Docker environment guide
│   └── AZURE_DEPLOYMENT.md      # Azure cloud deployment guide
├── infra/                        # Infrastructure as Code
│   ├── main.bicep               # Azure Bicep template
│   └── main.parameters.json     # Deployment parameters
├── monitoring/                   # Monitoring configuration
│   ├── prometheus.yml           # Prometheus config
│   ├── dashboard-local.json     # Grafana dashboard
│   └── datasources.yml          # Grafana datasources
├── reports/                      # Test reports and artifacts
├── assets/                       # Static assets (CSS, etc.)
├── docker-compose.yml            # Local Docker environment
├── Dockerfile.local              # Local development container
├── deploy-local.ps1             # Windows deployment script
├── deploy-local.sh              # Linux/macOS deployment script
├── health-check.ps1             # Environment health monitoring
├── requirements.txt             # Python dependencies
├── pytest.ini                  # pytest configuration
├── setup.cfg                    # Setup configuration
├── tox.ini                      # Tox configuration
└── validate_framework.py        # Framework validation script
```

## Installation

### Option 1: Local Development Setup

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

### Option 2: Docker Environment (Recommended)

**Prerequisites:**
- Docker Desktop installed and running
- At least 4GB RAM available for containers

**Quick Start:**
```powershell
# Windows PowerShell
.\deploy-local.ps1 -Build -Up

# Linux/macOS
./deploy-local.sh --build --up
```

This sets up a complete testing environment with:
- Selenium Grid (Chrome and Firefox nodes)
- Monitoring stack (Prometheus + Grafana)
- Allure reporting server
- File server for reports and artifacts

## Usage

### Running Tests with Docker (Recommended)

**Start the environment:**
```powershell
# Build and start all services
.\deploy-local.ps1 -Build -Up

# Wait for services to be ready
.\health-check.ps1 -Wait
```

**Run tests:**
```powershell
# Run all tests
.\deploy-local.ps1 -Test

# Run specific test file
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py"

# Run tests in parallel
.\deploy-local.ps1 -Test -Parallel

# Run specific test method
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py::TestE2ESearch::test_e2e_search_stock_symbol"
```

**Access Services:**
After starting the Docker environment, access these URLs:
- 🌐 **Selenium Grid Hub**: [http://localhost:4444](http://localhost:4444)
- 📊 **Test Reports**: [http://localhost:8080/reports/](http://localhost:8080/reports/)
- 🔥 **Allure Reports**: [http://localhost:5050](http://localhost:5050)
- 📈 **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000) (admin/admin123)
- 🔍 **Prometheus Metrics**: [http://localhost:9090](http://localhost:9090)

**Monitor and Debug:**
```powershell
# Check environment health
.\health-check.ps1 -Detailed

# View service status
.\deploy-local.ps1 -Status

# View logs
.\deploy-local.ps1 -Logs
.\deploy-local.ps1 -Logs -Service pytest-runner

# Stop environment
.\deploy-local.ps1 -Down
```

### Running Tests Locally (Alternative)

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

### Test Reports and Results

#### Docker Environment Reports
When using the Docker environment, reports are automatically generated and served:

1. **HTML Reports**: [http://localhost:8080/reports/html/](http://localhost:8080/reports/html/)
   - Traditional pytest HTML reports with detailed test results
   - Screenshots of failed tests included
   - Test duration and status information

2. **Allure Reports**: [http://localhost:5050](http://localhost:5050)
   - Interactive Allure reports with rich test insights
   - Test execution trends and history
   - Detailed step-by-step test execution
   - Test categorization and filtering

3. **JUnit XML**: Available at `./reports/junit-report.xml`
   - Standard JUnit format for CI/CD integration
   - Machine-readable test results

#### Local Development Reports
For local test execution:

**Generate and view Allure reports:**
```bash
# Run tests with allure
python -m pytest --alluredir=reports/allure-results

# Generate and serve report (requires allure command-line tool)
allure serve reports/allure-results
```

### Monitoring and Dashboards

#### Grafana Dashboard
Access the monitoring dashboard at [http://localhost:3000](http://localhost:3000):
- **Username**: admin
- **Password**: admin123

**Available Metrics:**
- Container resource usage (CPU, Memory)
- Selenium Grid status and session count
- Test execution rates and performance
- Network and disk I/O statistics
- Service health status

#### Prometheus Metrics
Raw metrics available at [http://localhost:9090](http://localhost:9090):
- Container performance metrics
- Application-specific metrics
- Custom test execution metrics
- Service availability monitoring

#### Health Monitoring
```powershell
# Quick health check
.\health-check.ps1

# Detailed health information
.\health-check.ps1 -Detailed

# Continuous monitoring (wait for healthy state)
.\health-check.ps1 -Wait -Timeout 300
```

### Test Scenarios

#### E2E Search Tests (`test_e2e_search.py`)

1. **Stock Symbol Search Test** - Tests complete search workflow for stock symbols
2. **Multiple Stocks Test** - Tests searching for multiple different stock symbols
3. **Error Handling Test** - Tests search functionality with invalid inputs
4. **Performance Test** - Tests search response times and performance

**Run E2E tests with Docker:**
```powershell
# Run all E2E search tests
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py"

# Run specific E2E test
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py::TestE2ESearch::test_e2e_search_stock_symbol"

# Run with parallel execution
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py" -Parallel
```

**Run E2E tests locally:**
```bash
# Run all E2E search tests
python -m pytest tests/test_e2e_search.py -v

# Run specific E2E test
python -m pytest tests/test_e2e_search.py::TestE2ESearch::test_e2e_search_stock_symbol -v

# Run with allure reporting
python -m pytest tests/test_e2e_search.py --alluredir=reports/allure-results
```

### Allure Reporting

#### Docker Environment (Automatic)
Allure reports are automatically generated and served at [http://localhost:5050](http://localhost:5050) when using Docker.

#### Local Development
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

### Docker Environment Management

#### Complete Environment Lifecycle
```powershell
# Build and start everything
.\deploy-local.ps1 -Build -Up

# Run comprehensive tests
.\deploy-local.ps1 -Test -Parallel

# Monitor health
.\health-check.ps1 -Detailed

# Clean shutdown
.\deploy-local.ps1 -Down

# Complete cleanup (removes containers and images)
.\deploy-local.ps1 -Clean
```

#### Service Management
```powershell
# Check all service status
.\deploy-local.ps1 -Status

# View logs for all services
.\deploy-local.ps1 -Logs

# View logs for specific service
.\deploy-local.ps1 -Logs -Service selenium-hub
.\deploy-local.ps1 -Logs -Service pytest-runner

# Restart specific service
docker-compose restart selenium-hub
```

#### Troubleshooting
```powershell
# Environment health check
.\health-check.ps1

# Detailed service information
.\health-check.ps1 -Detailed

# Wait for services to be ready (with timeout)
.\health-check.ps1 -Wait -Timeout 300

# View resource usage
docker stats

# Check service connectivity
docker-compose ps
```

## Configuration

### Docker Configuration
The Docker environment is configured through:
- **docker-compose.yml**: Service definitions and networking
- **Dockerfile.local**: Local development container configuration
- **monitoring/**: Grafana and Prometheus configurations

### pytest.ini
Main pytest configuration file with settings for:
- Test discovery patterns
- Allure integration
- HTML reporting
- JUnit XML output

### Browser Configuration

**Docker Environment:**
```powershell
# Uses Selenium Grid automatically with Chrome and Firefox nodes
.\deploy-local.ps1 -Test  # Runs on available browsers in the grid
```

**Local Development:**
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

### Core Dependencies
- **pytest**: Testing framework
- **selenium**: Web automation
- **allure-pytest**: Reporting
- **pyyaml**: YAML file handling
- **pytest-xdist**: Parallel execution
- **pytest-failed-screenshot**: Screenshot on failure

### Docker Environment
- **Docker Desktop**: Container runtime
- **Docker Compose**: Multi-container orchestration
- **Selenium Grid**: Distributed browser testing
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

### Cloud Deployment (Optional)
- **Azure CLI**: Cloud deployment tools
- **Azure Bicep**: Infrastructure as Code
- **Azure Container Instances**: Cloud container hosting

## Quick Start Examples

### Example 1: Complete Docker Setup
```powershell
# 1. Start environment
.\deploy-local.ps1 -Build -Up

# 2. Wait for services
.\health-check.ps1 -Wait

# 3. Run tests
.\deploy-local.ps1 -Test

# 4. View results
# - Test Reports: http://localhost:8080/reports/
# - Allure: http://localhost:5050
# - Monitoring: http://localhost:3000

# 5. Cleanup
.\deploy-local.ps1 -Down
```

### Example 2: Development Workflow
```powershell
# Start monitoring environment
.\deploy-local.ps1 -Build -Up

# Run specific test during development
.\deploy-local.ps1 -Test -TestPath "tests/test_e2e_search.py::TestE2ESearch::test_e2e_search_stock_symbol"

# Check logs if test fails
.\deploy-local.ps1 -Logs -Service pytest-runner

# View health status
.\health-check.ps1 -Detailed

# Continue development...
```

### Example 3: CI/CD Integration
```powershell
# Automated testing pipeline
.\deploy-local.ps1 -Build -Up
.\health-check.ps1 -Wait -Timeout 300
.\deploy-local.ps1 -Test -Parallel
.\deploy-local.ps1 -Down

# Reports available at:
# - ./reports/html/report.html
# - ./reports/junit-report.xml
# - ./reports/allure-results/
```

## Documentation

### Detailed Guides
- **[Local Docker Setup](docs/LOCAL_DOCKER_SETUP.md)**: Complete Docker environment guide
- **[Azure Deployment](docs/AZURE_DEPLOYMENT.md)**: Cloud deployment instructions

### Key Features Documentation
- **Selenium Grid**: Distributed browser testing with multiple nodes
- **Monitoring Stack**: Prometheus metrics and Grafana dashboards
- **Report Management**: Automated report generation and serving
- **Health Monitoring**: Comprehensive environment health checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.
