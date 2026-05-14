from ast import For

import allure
import pytest
from playwright.sync_api import expect

from Pages.HeatLog.heatLog import HeatLog
from Tests.test_base import BaseTest


@allure.feature("Heat Log")
@allure.story("Heat Log Navigation and Search")
class TestHeatLog(BaseTest):

    @allure.title("Test Heat Log Navigation After Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_heat_log_navigation_after_login(self, login):
        """
        Test navigation to Heat Log page after successful login
        """
        # Initialize page objects
        self.dashboard = login
        self.heat_log_page = HeatLog(login)

        self.dashboard.current_page.wait_for_timeout(6000)
        
        # Navigate to Heat Log page
        self.heat_log_page.navigate_to_heat_log(vessel_name)

        # Wait for search results to load
        self.dashboard.current_page.wait_for_timeout(6000)
        
        # Verify Heat Log page is loaded
        assert self.heat_log_page.is_heat_log_page_loaded()

    @allure.title("Test Vessel Name Search and Navigate to Heat Log Details")
    @allure.severity(allure.severity_level.NORMAL)
    def test_vessel_name_search_and_navigate_to_details(self, login):
        """
        Test searching for vessel name and navigating to heat log details page
        """
        # Initialize page objects
        self.dashboard = login
        self.heat_log_page = HeatLog(login)
        
        # Search for specific vessel (AMAGI GALAXY)
        vessel_name = "AMAGI GALAXY"

        # Navigate to Heat Log page
        self.heat_log_page.navigate_to_heat_log()

        # Wait for search results to load
        self.dashboard.current_page.wait_for_timeout(6000)
        
        # Verify Heat Log page is loaded
        assert self.heat_log_page.is_heat_log_page_loaded()
        
        # Search for specific vessel (AMAGI GALAXY)
        self.heat_log_page.search_heat_log(vessel_name)
        
        # Wait for search results to load
        self.dashboard.current_page.wait_for_timeout(2000)
        
        # Click on heat log row to view details
        self.heat_log_page.get_heat_log_view()
        
        # Wait for details page to load
        self.dashboard.current_page.wait_for_timeout(2000)
        
        # Verify navigation to details page (check URL or page elements)
        # This will depend on the actual details page structure
        # For now, we'll verify we're no longer on the listing page
        expect(self.heat_log_page.get_heat_log_title()).not_to_be_visible()
        
    

    