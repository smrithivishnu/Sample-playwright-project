# Playwright Python Automation Framework

A comprehensive automation framework built with Playwright, Python, and PyTest following the Page Object Model design pattern. This framework supports both UI and API testing with detailed reporting capabilities and advanced test execution ordering.

## Features

- **Multi-Browser Support**: Chromium, Firefox, WebKit, and Microsoft Edge
- **Page Object Model**: Clean and maintainable test architecture
- **Comprehensive Reporting**: HTML reports and Allure reports with test execution ordering
- **Advanced API Testing**: Integrated API testing with payload generation, logging, and verification
- **Configuration Management**: JSON-based configuration with test data management
- **Screenshot on Failure**: Automatic screenshots for failed tests
- **Test Data Management**: Centralized test data handling with Excel integration
- **Test Execution Ordering**: Custom pytest markers for controlled test sequence
- **API Logging**: Centralized API execution logging with request/response tracking

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
│   ├── excel_reader.py   # Excel file reader for port data
│   ├── api_logger.py     # Centralized API logging
│   ├── read_config.py    # Configuration reader
│   └── test_data_manager.py # Test data management
├── core/                 # Core framework components
│   ├── ai_engine.py      # AI engine for smart locators
│   ├── dom_analyzer.py   # DOM analysis utilities
│   └── smart_locator.py  # Smart locator implementation
├── allure-results/       # Allure test results
├── allure-report/        # Generated Allure reports
├── PortList.xlsx         # Port data for API testing
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

### Core Testing Framework
- **pytest==8.3.3**: Python testing framework
- **pytest-html==4.1.1**: HTML report generation
- **pytest-xdist==3.6.1**: Parallel test execution
- **pytest-order==1.2.1**: Test execution ordering

### Playwright Dependencies
- **playwright==1.48.0**: Browser automation library
- **pytest-playwright==0.5.0**: PyTest integration for Playwright

### Reporting
- **allure-pytest==2.13.5**: Allure reporting integration

### Data Processing
- **pandas==2.2.2**: Data manipulation and analysis
- **openpyxl==3.1.5**: Excel file handling

### HTTP Requests
- **requests==2.32.5**: HTTP client for API testing

### Built-in Modules
- `uuid`, `random`, `string`, `json`, `os`, `datetime`, `re`, `base64`, `difflib`

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
- Application URL and credentials
- API test data (vessel information, port functions, email data)
- Voyage configuration parameters
- Port count and test scenarios data

### Port Data (PortList.xlsx)
Excel file containing port data for API testing:
- Port codes, names, and countries
- Used for voyage itinerary payload generation
- Fallback data available if Excel reading fails

## Running Tests

### UI Test Execution
```bash
pytest --alluredir=allure-results Tests/login/test_logout.py::TestLogout Tests/login/test_login.py::TestLogin
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

### API Test Execution
```bash
# Run all API tests
pytest --alluredir=allure-results Tests/api/

# Run specific voyage itinerary tests
pytest --alluredir=allure-results Tests/api/test_voyage_itinerary.py

# Run with test execution ordering
pytest --alluredir=allure-results Tests/api/test_voyage_itinerary.py -v
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
- **Voyage Itinerary API**: Comprehensive voyage management testing
  - Initial voyage creation
  - Port management (add, update, delete)
  - Status updates and voyage modifications
  - Port function updates
  - Estimate ID management
- **Authentication API**: Login/logout endpoints

## Reporting

### Allure Reports
- Interactive and detailed reports with test execution ordering
- Test execution history and timeline
- Screenshots and attachments
- API request/response logging
- Generated in `allure-report/`

### API Logging
- Centralized API execution logging in `api_execution_log.txt`
- Request/response payload tracking
- Test case correlation with API calls
- Automatic log clearing before test execution

### Test Execution Ordering
- Custom pytest markers (`@pytest.mark.run(order=X)`)
- Controlled test sequence for API tests
- Proper test dependency management
- Allure report displays tests in execution order

## Best Practices

1. **Page Object Model**: All page interactions should go through page objects
2. **Test Data Management**: Use centralized test data configuration
3. **Reporting**: Always generate reports for test results
4. **Screenshots**: Failed tests automatically capture screenshots
5. **API Testing**: Use centralized logging for API request/response tracking
6. **Test Ordering**: Use pytest markers for controlled test execution sequence
7. **Port Data**: Use Excel-based port selection with proper fallback handling

## Contributing

1. Follow the existing code structure and patterns
2. Add new page objects in the `Pages/` directory
3. Add new tests in appropriate subdirectories under `Tests/`
4. Update test data in `test_data.json` when needed
5. Ensure all tests pass before submitting

## Troubleshooting

### Common Issues
- **Browser not found**: Run `playwright install` to install browsers
- **Import errors**: Ensure all dependencies are installed from `requirements.txt`
- **Timeout issues**: Adjust timeout values in `config.json`
- **API test failures**: Check `api_execution_log.txt` for detailed request/response logs
- **Port data issues**: Verify `PortList.xlsx` exists and has proper format
- **Test ordering issues**: Ensure `@pytest.mark.run(order=X)` markers are properly configured
- **Allure report ordering**: Tests will display in execution order with proper markers

### Debug Mode
Set `Headless` to `False` in `config.json` to watch tests execute in real-time.

### API Debugging
- Check `api_execution_log.txt` for detailed API logs
- Verify port data in `PortList.xlsx` if same ports appear in payloads
- Ensure test data configuration in `test_data.json` is correct

### Test Execution Issues
- Verify pytest markers are registered (check for "Unknown pytest.mark.run" warnings)
- Ensure test dependencies are properly ordered
- Check Allure report for test execution sequence