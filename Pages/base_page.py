from playwright.sync_api import Page, Locator
from core.smart_locator import SmartActions

class BasePage:

    def __init__(self, page: Page):
        self.current_page = page
        self.ai = SmartActions(page)

    def user_profile(self) -> Locator:
        return self.current_page.locator(Selectors.UserProfile)

class Selectors:
    UserProfile = "a.profile-container"




