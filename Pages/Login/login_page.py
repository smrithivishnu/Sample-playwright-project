from playwright.sync_api import Page, Locator

from Pages.Dashboard.dashboard import Dashboard
from Pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self._selectors = self._Selectors()

    def set_username(self, value: str):
        username = self.ai.locator(self._selectors.USERNAME)
        username.click()
        username.fill(value)

    def set_password(self, value: str):
        username = self.ai.locator(self._selectors.PASSWORD)
        username.click()
        username.fill(value)

    def click_login(self):
        self.ai.click(self._selectors.LOGIN_BUTTON)

    def click_externallogin(self):
        self.ai.click(self._selectors.EXTERNALUSER_BUTTON)

    def click_loginMainPage(self):
        self.ai.click(self._selectors.LOGIN_BACKBUTTON)

    def login_to_application(self, username: str, password: str) -> Dashboard:
        self.click_externallogin()
        self.set_username(username)
        self.set_password(password)
        self.click_login()
        return Dashboard(self.current_page)

    def get_error_locator(self) -> Locator:
        return self.ai.locator(self._selectors.ERROR_MSG)

    def get_login_button_locator(self) -> Locator:
        return self.ai.locator(self._selectors.EXTERNALUSER_BUTTON)

    class _Selectors:
        USERNAME = "input[formcontrolname='userName']"
        PASSWORD = "input[type='password']"
        LOGIN_BUTTON = "button[label='Submit']"
        EXTERNALUSER_BUTTON = "button:has-text('Login as External User')"
        LOGIN_BACKBUTTON = "a.back-nav:has-text('Back to previous page')"
        ERROR_MSG = ".p-toast-detail:has-text('Bad credentials')"



