from playwright.sync_api import Page, Locator
from Pages.base_page import BasePage


class ProductsListPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._selectors = self._Selectors()

    # region burger menu item
    def click_burger_menu(self):
        self.ai.click(self._selectors.PROFILE_BUTTON)

    def click_logout(self):
        self.ai.click(self._selectors.LOGOUT_BUTTON)
        from Pages.Login.login_page import LoginPage
        return LoginPage(self.current_page)

    class _Selectors:
        PROFILE_BUTTON = "a.profile-container"
        LOGOUT_BUTTON = "li:has(i.pi-sign-out)"
