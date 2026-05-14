import base64
import pytest
import allure

from Pages.Login.login_page import LoginPage
from Utilities.read_config import AppConfiguration
from Utilities.test_data_manager import TestDataManager
from playwright.sync_api import sync_playwright
from Pages.Dashboard.dashboard import Dashboard
from API.endpoints.auth_api import AuthAPI


@pytest.fixture(scope="session")
def api_client():
    test_data = TestDataManager.get_common_info()
    base_url = test_data["Url"]
    return AuthAPI(base_url)

def get_browser(browser_name, playwright, launch_options):
    match browser_name:
        case "chromium":
            return playwright.chromium.launch(**launch_options, args=['--start-maximized'])
        case "firefox":
            return playwright.firefox.launch(**launch_options)
        case "msedge":
            return playwright.chromium.launch(channel='msedge', **launch_options, args=['--start-maximized'])
        case "webkit":
            return playwright.webkit.launch(**launch_options)
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.fixture(scope="session")
def setup(request, setup_browser):
    configuration = AppConfiguration.get_app_configuration()
    test_data = TestDataManager.get_common_info()
    base_url = test_data["Url"]

    headless = eval(configuration["Headless"])
    slow_mo = float(configuration["SlowMo"])
    launch_options = {"headless": headless, "slow_mo": slow_mo}

    playwright = sync_playwright().start()
    browser = get_browser(setup_browser, playwright, launch_options)

    context = browser.new_context(no_viewport=True)
    page = context.new_page()

    page.goto(base_url)
    
    # Store playwright instance on the page object for later use
    page._playwright = playwright
   
    request.session.page = page

    yield page

    # Close only once after ALL tests finish
    context.close()
    browser.close()
    playwright.stop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends PyTest to take and embed screenshot in HTML report whenever test fails.
    """
    outcome = yield
    report = outcome.get_result()

    pytest_html = item.config.pluginmanager.getplugin("html")
    extra = getattr(report, "extras", [])

    # Only take screenshot during actual test execution
    if report.when == "call" and report.failed:
        page = item.funcargs.get("setup", None)

        if page:
            try:
                screenshot_bytes = page.screenshot()
                extra.append(
                    pytest_html.extras.image(
                        base64.b64encode(screenshot_bytes).decode(),
                        "Screenshot"
                    )
                )
            except Exception:
                pass

    report.extras = extra

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("setup", None)

        if page:
            try:
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

@pytest.fixture(scope="session")
def login(request, setup) -> Dashboard:
    test_data = TestDataManager.get_common_info()

    username = test_data["ValidUserName"]
    password = test_data["ValidPassword"]
    login = LoginPage(setup)
    login.login_to_application(username, password)
    return Dashboard(setup)


def pytest_addoption(parser):
    parser.addoption("--browser-name", action="store", default="chromium", help="Browser to run tests with (chromium, "
                                                                                "firefox, webkit, edge)")


@pytest.fixture(scope="session")
def setup_browser(request):
    """
    :return: This will return the browser name to setup method
    """
    return request.config.getoption("--browser-name")
