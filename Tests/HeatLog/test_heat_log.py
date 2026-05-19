from ast import For

import allure
import pytest
from playwright.sync_api import expect, sync_playwright

from Pages.HeatLog.heatLog import HeatLog
from Pages.Login.login_page import LoginPage
from Pages.Dashboard.dashboard import Dashboard
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
        
        ports = self.heat_log_page.heat_log_details_page_itinerary_ports_details()
        print(f"Total ports extracted: {len(ports)}")
        for i, port_name in enumerate(ports):
            print(f"Port {i}: {port_name}")
        
        # Verify ports list is not empty
        assert len(ports) > 0, "No ports found in itinerary"

    @allure.title("Test Shore to Vessel Port Details Synchronization")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_shore_to_vessel_port_details_synchronization(self, login, vessel_login):
        """
        Test that port details are synchronized between shore and vessel instances
        after 2-5 minutes of communication wait time.
        """
        # Initialize shore instance page objects
        self.dashboard = login
        self.heat_log_page_shore = HeatLog(login)
        
        test_data = TestDataManager.get_test_data()
        vessel_name = test_data["vessel_data"]["VIP_VSL_NAME"]
        vessel_code = test_data["vessel_data"]["VIP_VSL_CODE"]

        # Extract port details from shore instance
        self.heat_log_page_shore.navigate_to_heat_log()
        self.dashboard.current_page.wait_for_timeout(500)
        assert self.heat_log_page_shore.is_heat_log_page_loaded()
        
        self.heat_log_page_shore.search_heat_log(vessel_name)
        self.dashboard.current_page.wait_for_timeout(500)
        
        self.heat_log_page_shore.get_heat_log_view(vessel_code)
        self.dashboard.current_page.wait_for_timeout(500)
        
        assert self.heat_log_page_shore.is_heat_log_details_page_loaded()
        self.dashboard.current_page.wait_for_timeout(500)
        
        shore_ports = self.heat_log_page_shore.heat_log_details_page_itinerary_ports_details()
        print(f"Shore - Total ports extracted: {len(shore_ports)}")
        for i, port_name in enumerate(shore_ports):
            print(f"Shore - Port {i}: {port_name}")
        
        assert len(shore_ports) > 0, "No ports found in shore itinerary"

        # Use vessel_login fixture for vessel instance (already logged in)
        vessel_page = vessel_login
        vessel_heat_log_page = HeatLog(vessel_page)
            
        # Extract port details from vessel instance
        vessel_heat_log_page.navigate_to_heat_log()
        vessel_page.wait_for_timeout(500)
        assert vessel_heat_log_page.is_heat_log_page_loaded()
            
        vessel_heat_log_page.get_heat_log_view(vessel_code)
        vessel_page.wait_for_timeout(500)
            
        assert vessel_heat_log_page.is_heat_log_details_page_loaded()
            
        # Wait for communication from shore to vessel (2-5 minutes)
        print("Waiting 3 minutes for shore to vessel communication...")
        vessel_page.wait_for_timeout(180000)  # 3 minutes
            
        # Refresh vessel page and extract port details again
        vessel_page.reload()
        vessel_page.wait_for_timeout(500)
            
        vessel_ports_after_sync = vessel_heat_log_page.heat_log_details_page_itinerary_ports_details()
        print(f"Vessel (after sync) - Total ports extracted: {len(vessel_ports_after_sync)}")
        for i, port_name in enumerate(vessel_ports_after_sync):
            print(f"Vessel (after sync) - Port {i}: {port_name}")
            
        # Compare shore and vessel port details
        print("\n=== Comparing Shore and Vessel Port Details ===")
        print(f"Shore ports count: {len(shore_ports)}")
        print(f"Vessel ports count (after sync): {len(vessel_ports_after_sync)}")
            
        # Check if port counts match
        assert len(shore_ports) == len(vessel_ports_after_sync), \
                f"Port count mismatch: Shore has {len(shore_ports)}, Vessel has {len(vessel_ports_after_sync)}"
            
        # Check if port details match
        ports_match = True
        for i, (shore_port, vessel_port) in enumerate(zip(shore_ports, vessel_ports_after_sync)):
            if shore_port != vessel_port:
                ports_match = False
                print(f"Mismatch at port {i}: Shore='{shore_port}', Vessel='{vessel_port}'")
            
        assert ports_match, "Port details do not match between shore and vessel instances"
        print(" Port details match successfully between shore and vessel instances")