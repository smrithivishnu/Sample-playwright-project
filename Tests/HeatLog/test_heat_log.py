from ast import For

import allure
import pytest
from playwright.sync_api import expect

from Pages.HeatLog.heatLog import HeatLog
from Tests.test_base import BaseTest
from Utilities.test_data_manager import TestDataManager


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
        
        test_data = TestDataManager.get_test_data()
        vessel_name = test_data["vessel_data"]["VIP_VSL_NAME"]

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
        
        test_data = TestDataManager.get_test_data()
        vessel_name = test_data["vessel_data"]["VIP_VSL_NAME"]

        # Navigate to Heat Log page
        self.heat_log_page.navigate_to_heat_log()

        # Wait for search results to load
        self.dashboard.current_page.wait_for_timeout(500)
        
        # Verify Heat Log page is loaded
        assert self.heat_log_page.is_heat_log_page_loaded()
        
        # Search for specific vessel (AMAGI GALAXY)
        self.heat_log_page.search_heat_log(vessel_name)
        
        # Wait for search results to load
        self.dashboard.current_page.wait_for_timeout(500)
        
        # Click on heat log row to view details
        self.heat_log_page.get_heat_log_view(vessel_name)
        
        # Wait for details page to load
        self.dashboard.current_page.wait_for_timeout(500)
        
         # Verify Heat Log page is loaded
        assert self.heat_log_page.is_heat_log_details_page_loaded()

        self.dashboard.current_page.wait_for_timeout(5000)
        
        ports = self.heat_log_page.heat_log_details_page_itinerary_dates()
        print(f"Total ports extracted: {len(ports)}")
        for i, port_name in enumerate(ports):
            print(f"Port {i}: {port_name}")
        
        # Verify ports list is not empty
        assert len(ports) > 0, "No ports found in itinerary"
       

        
    