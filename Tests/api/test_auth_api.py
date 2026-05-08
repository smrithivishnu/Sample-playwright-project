from Utilities.test_data_manager import TestDataManager
from Tests.test_base import BaseTest
from API.endpoints.auth_api import AuthAPI
import allure
import base64
from playwright.sync_api import expect

class TestAPI(BaseTest):

    test_data = TestDataManager.get_common_info()
    def get_user_credentials(self, user_type):
        return {
            "username": self.test_data[user_type + "UserName"],
            "password": self.test_data[user_type + "Password"]
        }

    @allure.step("Login via API")
    def test_login_api(self, api_client):

        creds = self.get_user_credentials("Valid")
        response = api_client.login(creds["username"], base64.b64encode(creds["password"].encode()).decode())
        assert response.status_code == 200
       
        # Parse JSON response once to avoid consuming the stream twice
        try:
            response_json = response.json()
            AuthAPI.log_response(response)
            token = response_json["jwtToken"]
            api_client.client.set_token(token)
        except Exception as e:
            print(f"Error parsing login response: {e}")
            print(f"Response text: {response.text}")
            raise
        return response
    
    @allure.step("Bunker Consumption Vessel wise via API")
    def test_bunker_consumption_vessel_api(self, api_client):

        response = api_client.bunker_consumption_vessel("DAILY",20,False)
        assert response.status_code == 200
       
        AuthAPI.log_response(response)
        return response

    @allure.step("Inventory ROB Summary via API")
    def test_inventory_rob_summary_api(self, api_client):

        response = api_client.inventory_rob_summary()
        assert response.status_code == 200
       
        AuthAPI.log_response(response)
        return response

        
    