# Playwright Python Automation Framework

A comprehensive automation framework built with Playwright, Python, and PyTest following the Page Object Model design pattern. This framework supports both UI and API testing with detailed reporting capabilities.

## Features

- **Multi-Browser Support**: Chromium, Firefox, WebKit, and Microsoft Edge
- **Page Object Model**: Clean and maintainable test architecture
- **Comprehensive Reporting**: HTML reports and Allure reports
- **API Testing**: Integrated API testing capabilities
- **Configuration Management**: JSON-based configuration
- **Screenshot on Failure**: Automatic screenshots for failed tests
- **Test Data Management**: Centralized test data handling

## Project Structure

```
Sample-playwright-project/
├── API/                    # API testing components
│   ├── clients/           # API client implementations
│   ├── endpoints/         # API endpoint definitions
│   └── payloads/          # API request payloads
├── Pages/                 # Page Object Model implementation
│   ├── Login/            # Login page objects
│   ├── Products/         # Products page objects
│   └── base_page.py      # Base page class
├── Tests/                 # Test cases
│   ├── api/              # API tests
│   ├── login/            # Login tests
│   ├── products/         # Products tests
│   ├── conftest.py       # PyTest configuration and fixtures
│   └── test_base.py      # Base test class
├── Utilities/            # Utility modules
│   ├── read_config.py    # Configuration reader
│   └── test_data_manager.py # Test data management
├── allure-results/       # Allure test results
├── allure-report/        # Generated Allure reports
├── config.json          # Framework configuration
├── test_data.json       # Test data
├── pytest.ini           # PyTest configuration
└── requirements.txt     # Python dependencies
```

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Dependencies

- **playwright==1.48.0**: Browser automation library
- **pytest==8.3.3**: Python testing framework
- **pytest-html==4.1.1**: HTML report generation
- **pytest-playwright==0.5.0**: PyTest integration for Playwright
- **pytest-xdist==3.6.1**: Parallel test execution
- **allure-pytest==2.13.5**: Allure reporting integration

## Configuration

### Framework Configuration (config.json)
```json
{
    "Headless": "False",
    "SlowMo": "0",
    "DefaultNavigationTimeout": "120000",
    "DefaultTimeout": "60000"
}
```

### Test Data (test_data.json)
Test data is centralized in `test_data.json` and includes:
- Application URL
- Valid/Invalid user credentials
- Test scenarios data

## Running Tests

### Basic Test Execution
```bash
pytest
```
### Browser-Specific Execution
Run tests on specific browsers:
```bash
# Firefox
pytest --browser-name firefox

# Microsoft Edge
pytest --browser-name msedge

# WebKit
pytest --browser-name webkit

# Chromium (default)
pytest --browser-name chromium
```

### Generate Allure Reports
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## Test Categories

### UI Tests
- **Login Tests**: Authentication functionality
- **Products Tests**: Product management features
- **Navigation Tests**: Page navigation and routing

### API Tests
- **Authentication API**: Login/logout endpoints
- **Products API**: CRUD operations for products

## Reporting

### Allure Reports
- Interactive and detailed reports
- Test execution history
- Screenshots and attachments
- Generated in `allure-report/`

## Best Practices

1. **Page Object Model**: All page interactions should go through page objects
2. **Test Data Management**: Use centralized test data configuration
3. **Reporting**: Always generate reports for test results
4. **Screenshots**: Failed tests automatically capture screenshots

## Contributing

1. Follow the existing code structure and patterns
2. Add new page objects in the `Pages/` directory
3. Add new tests in appropriate subdirectories under `Tests/`
4. Update test data in `test_data.json` when needed
5. Ensure all tests pass before submitting

## Troubleshooting

### Common Issues
- **Browser not found**: Run `playwright install` to install browsers
- **Import errors**: Ensure all dependencies are installed
- **Timeout issues**: Adjust timeout values in `config.json`

### Debug Mode
Set `Headless` to `False` in `config.json` to watch tests execute in real-time.