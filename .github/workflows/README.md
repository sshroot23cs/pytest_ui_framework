# 🚀 GitHub Actions Workflows

This directory contains automated CI/CD workflows for the pytest UI automation framework.

## 📋 Available Workflows

### 🧪 PR Tests (`pr-tests.yml`)
**Trigger**: Pull requests to main/master branch
**Purpose**: Comprehensive testing before merging

**Features**:
- ✅ Code quality checks (Black, isort, Flake8)
- 🌐 Multi-browser testing (Chrome & Firefox)
- 🐳 Docker environment validation
- 📊 Allure report generation
- 📤 Test artifact uploads
- 📋 PR status summary

**Jobs**:
1. **Code Quality**: Formatting, linting, validation
2. **Chrome E2E Tests**: Full test suite in Chrome
3. **Firefox E2E Tests**: Full test suite in Firefox  
4. **Docker Tests**: Container-based testing
5. **Test Summary**: Consolidated results
6. **PR Status Check**: Pass/fail determination

### 🚀 CI (`ci.yml`)
**Trigger**: Push to main/master, daily schedule, manual
**Purpose**: Continuous integration for main branch

**Features**:
- 🔄 Matrix testing (Chrome & Firefox)
- ⏰ Scheduled daily runs (2 AM UTC)
- 🎯 Manual execution with parameters
- 📊 Streamlined reporting

### 🎯 Manual Tests (`manual-tests.yml`)
**Trigger**: Manual workflow dispatch
**Purpose**: On-demand testing with custom parameters

**Parameters**:
- **Test File**: Choose specific test files
- **Browser**: Chrome, Firefox, or both
- **Headless**: Enable/disable headless mode
- **Parallel**: Run tests in parallel
- **Environment**: Test environment simulation

### 📊 Health Check (`health-check.yml`)
**Trigger**: Changes to workflows, requirements, or source code
**Purpose**: Basic repository validation

**Checks**:
- ✅ Framework validation script
- 📁 File structure integrity
- 🔍 Module import capability
- 📋 Health status reporting

## 🎛️ Workflow Configuration

### Environment Variables
```yaml
PYTHON_VERSION: '3.12'
NODE_VERSION: '18'
HEADLESS: true
DISPLAY: :99
```

### Required Secrets
No additional secrets required - workflows use public actions and tools.

### Branch Protection
Recommended branch protection rules for `main`:
- ✅ Require status checks to pass
- ✅ Require PR reviews
- ✅ Include administrators
- ✅ Restrict push access

## 📊 Test Reports

### Allure Reports
- 🌐 **Interactive reports** with step-by-step execution
- 📈 **Trend analysis** and history tracking
- 📊 **Rich dashboards** with metrics
- 📸 **Screenshot attachments** on failures

### HTML Reports
- 📄 **Self-contained** reports (no dependencies)
- 🎨 **Styled output** with embedded CSS
- 📱 **Mobile-friendly** responsive design

### JUnit XML
- 🔧 **CI/CD integration** compatible
- 📈 **Test result parsing** for external tools
- 🏷️ **Test categorization** and metadata

## 📁 Artifacts

### Retention Policies
- **PR Tests**: 30 days
- **CI Tests**: 7 days  
- **Manual Tests**: 30 days
- **Health Checks**: No artifacts

### Artifact Contents
```
reports/
├── allure-results/     # Raw Allure data
├── allure-report/      # Generated HTML reports
├── junit-report.xml    # JUnit test results
├── html-report.html    # Self-contained HTML
└── screenshots/        # Failure screenshots
```

## 🚀 Usage Examples

### Triggering PR Tests
```bash
# Create PR - tests run automatically
git checkout -b feature/new-test
git push origin feature/new-test
# Create PR via GitHub UI
```

### Manual Test Execution
1. Go to **Actions** tab in GitHub
2. Select **🎯 Manual Test Execution**
3. Click **Run workflow**
4. Configure parameters:
   - Test file: `tests/test_e2e_search.py`
   - Browser: `chrome`
   - Headless: `true`
   - Parallel: `false`
5. Click **Run workflow**

### Viewing Results
1. **Workflow Summary**: Check GitHub Actions page
2. **Job Logs**: Click on individual jobs for details
3. **Artifacts**: Download test reports and screenshots
4. **Step Summary**: View consolidated results

## 🔧 Customization

### Adding New Browsers
```yaml
strategy:
  matrix:
    browser: [chrome, firefox, safari, edge]
```

### Custom Test Paths
```yaml
inputs:
  test_path:
    description: 'Custom test path'
    default: 'tests/custom/'
```

### Environment-Specific Config
```yaml
env:
  CUSTOM_VAR: ${{ secrets.CUSTOM_SECRET }}
  TEST_URL: "https://staging.example.com"
```

## 🛠️ Troubleshooting

### Common Issues
1. **Browser Setup Fails**: Check browser action versions
2. **Tests Timeout**: Increase timeout in pytest config
3. **Artifact Upload Fails**: Check path specifications
4. **Allure Generation Fails**: Ensure Node.js setup

### Debug Steps
1. Enable verbose logging in pytest
2. Check workflow logs in Actions tab
3. Download artifacts for local analysis
4. Review test output in job summaries

## 📈 Monitoring

### Workflow Status
- **Badge**: Add workflow status badges to README
- **Notifications**: Configure GitHub notifications
- **Integrations**: Connect to Slack/Teams for alerts

### Performance Metrics
- **Execution Time**: Monitor workflow duration
- **Success Rate**: Track test pass/fail ratios
- **Resource Usage**: Monitor runner utilization

---

*Last Updated: September 28, 2025*