from playwright.sync_api import Page, Locator
from typing import List
from Pages.base_page import BasePage


class HeatLog(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._selectors = self._Selectors()

    # region HeatLog specific functions
    def navigate_to_heat_log(self):
        """Navigate to HeatLog page"""
        self.ai.click(self._selectors.HEAT_LOG_MENU)
    
    # region HeatLog specific functions
    def navigate_to_heat_log_vessel_card_search(self, search_term: str):
        """Navigate to HeatLog page"""
        self.ai.fill(self._selectors.COMMON_VESSEL_SEARCH, search_term)
        self.ai.press("Enter")
        self.ai.click(self._selectors.HEAT_LOG_VIEW_LINK)

    # def click_add_heat_log(self):
    #     """Click on Add Heat Log button"""
    #     self.ai.click(self._selectors.ADD_HEAT_LOG_BUTTON)

    # def click_edit_heat_log(self, log_id: str):
    #     """Click on Edit Heat Log for specific log ID"""
    #     self.ai.click(f"{self._selectors.EDIT_HEAT_LOG_BUTTON}[data-log-id='{log_id}']")

    # def click_delete_heat_log(self, log_id: str):
    #     """Click on Delete Heat Log for specific log ID"""
    #     self.ai.click(f"{self._selectors.DELETE_HEAT_LOG_BUTTON}[data-log-id='{log_id}']")

    def search_heat_log(self, search_term: str):
        """Search for heat log by search term"""
        self.ai.click(self._selectors.FILTER_ICON_VESSEL_NAME)
        self.ai.fill(self._selectors.VESSEL_NAME_SEARCH_INPUT, search_term)
        self.ai.press("Enter")

    def get_heat_log_view(self, vessel_name: str) -> Locator:
        """Get heat log table locator"""
        self.ai.click(self._selectors.HEAT_LOG_ROW_VIEW.replace("VESSEL NAME", vessel_name))

    def is_heat_log_page_loaded(self) -> bool:
        """Check if HeatLog page is loaded"""
        return self.ai.is_visible(self._selectors.HEAT_LOG_TITLE)
    
    def is_heat_log_details_page_loaded(self) -> bool:
        """Check if HeatLog details page is loaded"""
        return self.ai.is_visible(self._selectors.HEAT_LOG_DETAILS_PAGE_TITLE)
    
    def heat_log_details_page_itinerary_ports(self) -> List[str]:
        """
        Extract all port names from the HeatLog itinerary timeline.
        
        Returns:
            List[str]: List of port names extracted from the itinerary
        """
        return self.ai.locatorMultipleElements(self._selectors.HEAT_LOG_ITINERARY, self._selectors.HEAT_LOG_ITINERARY_PORT_NAME)
    
    def heat_log_details_page_itinerary_dates(self) -> List[str]:
        """
        Extract all port names from the HeatLog itinerary timeline.
        
        Returns:
            List[str]: List of port names extracted from the itinerary
        """
        return self.ai.locatorMultipleElements(self._selectors.HEAT_LOG_ITINERARY, self._selectors.HEAT_LOG_ITINERARY_PORT_NAME)
    
    def heat_log_details_page_itinerary_dates(self) -> List[str]:
        """
        Extract all port dates from the HeatLog itinerary timeline.

        Returns:
            List[str]: List of port dates extracted from the itinerary
        """
        return self.ai.locatorMultipleElements(self._selectors.HEAT_LOG_ITINERARY, self._selectors.HEAT_LOG_ITINERARY_PORT_TIME)

    class _Selectors: 
        COMMON_VESSEL_SEARCH = "input.vessel-search-input[placeholder='Search Vessel...']"
        HEAT_LOG_VIEW_LINK = "img[src='/assets/img/heat_log_icon.svg']"
        HEAT_LOG_MENU = "li:has-text('Temp, O₂ & Pressure Monitoring')"
        FILTER_ICON_VESSEL_NAME = "th[data-field='vesselName'] button[aria-label='Show Filter Menu']"
        EDIT_HEAT_LOG_BUTTON = "button:has-text('Edit')"
        DELETE_HEAT_LOG_BUTTON = "button:has-text('Delete')"
        VESSEL_NAME_SEARCH_INPUT = ".p-column-filter-constraints input.p-inputtext"
        HEAT_LOG_TITLE = "a:has-text('Temp, O₂ & Pressure Monitoring Log Listing')"
        HEAT_LOG_ROW_VIEW = "tr:has(td:first-child:text-is('VESSEL NAME'))"
        HEAT_LOG_DETAILS_PAGE_TITLE = "h3:has-text('Ongoing Log Details')"
        HEAT_LOG_ITINERARY = "swiper-slide"
        HEAT_LOG_ITINERARY_PORT_NAME = "div.port b"
        HEAT_LOG_ITINERARY_PORT_TIME = ".port-time-value"