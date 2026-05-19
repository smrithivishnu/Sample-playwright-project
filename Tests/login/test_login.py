import allure

from Pages.Login.login_page import LoginPage
from Pages.Dashboard.dashboard import Dashboard
from Tests.login.test_logout import TestLogout
from Tests.test_base import BaseTest
from Utilities.test_data_manager import TestDataManager
from playwright.sync_api import expect


@allure.feature("Login")
@allure.story("Validate Login")
class TestLogin(BaseTest):

    test_data = TestDataManager.get_common_info()

    def get_user_credentials(self, user_type):
        return {
            "username": self.test_data[user_type + "UserName"],
            "password": self.test_data[user_type + "Password"]
        }
    
    @allure.title("Verify user cannot login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_invalid_credentials(self, setup):
        """
        Verify login with invalid credentials.
        """
        expected_error_msg = "Bad credentials or user not found"

        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Invalid")

        # Perform login
        self.login_page.click_externallogin()
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_locator()
        expect(actual_msg).to_have_text(expected_error_msg)
        self.login_page.click_loginMainPage()

    @allure.title("Verify user cannot login with locked user credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_locked_user(self, setup):
        """
        Verify login with a locked user.
        """
        expected_error_msg = "Bad credentials or user not found"

        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Locked")

        # Perform login
        self.login_page.click_externallogin()
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the appropriate error message is displayed
        actual_msg = self.login_page.get_error_locator()
        expect(actual_msg).to_have_text(expected_error_msg)
        self.login_page.click_loginMainPage()

    @allure.title("Verify user can login with valid user credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_valid_credentials(self,setup):
        """
        Verify login with valid credentials.
        """
        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Valid")

        # Perform login
        self.login_page.click_externallogin()
        self.login_page.login_to_application(creds["username"], creds["password"])

        # Verify that the user is navigated to the Dashboard page
        expect(self.login_page.user_profile()).to_be_visible()
        # Click on the burger menu and log out
        products_page = Dashboard(setup)
        products_page.click_burger_menu()
        products_page.click_logout()
        

    @allure.title("Verify username is not case sensitive - lowercase")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_lowercase_username(self, setup):
        """
        Verify login with valid credentials using lowercase username.
        """
        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Valid")
        
        # Convert username to lowercase
        lowercase_username = creds["username"].lower()
        
        # Perform login with lowercase username
        self.login_page.click_externallogin()
        self.login_page.login_to_application(lowercase_username, creds["password"])
        
        # Verify that the user is navigated to the Dashboard page
        expect(self.login_page.user_profile()).to_be_visible()
        # Click on the burger menu and log out
        products_page = Dashboard(setup)
        products_page.click_burger_menu()
        products_page.click_logout()
        

    @allure.title("Verify username is not case sensitive - uppercase")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_uppercase_username(self, setup):
        """
        Verify login with valid credentials using uppercase username.
        """
        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Valid")
        
        # Convert username to uppercase
        uppercase_username = creds["username"].upper()
        
        # Perform login with uppercase username
        self.login_page.click_externallogin()
        self.login_page.login_to_application(uppercase_username, creds["password"])
        
        # Verify that the user is navigated to the Dashboard page
        expect(self.login_page.user_profile()).to_be_visible()
        
       # Click on the burger menu and log out
        products_page = Dashboard(setup)
        products_page.click_burger_menu()
        products_page.click_logout()
        

    @allure.title("Verify username is not case sensitive - mixed case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_mixedcase_username(self, setup):
        """
        Verify login with valid credentials using mixed case username.
        """
        self.login_page = LoginPage(setup)
        creds = self.get_user_credentials("Valid")
        
        # Convert username to mixed case (capitalize first letter, lowercase rest)
        mixedcase_username = creds["username"].capitalize()
        
        # Perform login with mixed case username    
        self.login_page.click_externallogin()
        self.login_page.login_to_application(mixedcase_username, creds["password"])
        
        # Verify that the user is navigated to the Dashboard page
        expect(self.login_page.user_profile()).to_be_visible()
        # Click on the burger menu and log out
        products_page = Dashboard(setup)
        products_page.click_burger_menu()
        products_page.click_logout()
   
