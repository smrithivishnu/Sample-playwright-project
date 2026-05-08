from pickle import NONE
from API.clients.api_client import APIClient
from API.payloads.auth_payloads import AuthPayloads
import allure
import json

class AuthAPI:

    def __init__(self, base_url):
        self.client = APIClient(base_url)

    def set_middleware_token(self, token):
        """Set middleware token for specific APIs"""
        self.client.session.headers.update({
            "mwToken": token
        })

    def log_response(response):
        print("\n--- API RESPONSE ---")
        print("Status:", response.status_code)
        try:
            response_json = response.json()
            print(json.dumps(response_json, indent=4))
            allure.attach(
            json.dumps(response_json, indent=4),
            name="API Response",
            attachment_type=allure.attachment_type.JSON
            )
        except Exception as e:
            print(f"Could not parse JSON response: {e}")
            print(response.text)

    def log_request(self, method, endpoint, headers=None, json_data=None):
        """Log API request details for debugging"""
        print("\n--- API REQUEST ---")
        print("Method:", method)
        print("Endpoint:", endpoint)
        print("Headers:", headers or self.client.session.headers)
        if json_data:
            print("Request Body:")
            print(json.dumps(json_data, indent=4))
            allure.attach(
                json.dumps(json_data, indent=4),
                name="API Request",
                attachment_type=allure.attachment_type.JSON
            )

    def login(self, username, password):
        payload = AuthPayloads.login_payload(username, password)
        return self.client.post("/auth/v1/login", json=payload)
    
    def bunker_consumption_vessel(self, range, limit, favVessel):
        payload = AuthPayloads.bunker_consumption_vessel_payload(range, limit, favVessel)
        return self.client.post("/monitor/dashboard/v1/bunker-consumption-vessel", json=payload)
    
    def inventory_rob_summary(self):
        return self.client.get("/api/inventory/dashboard/v1/rob/summary/2026/false")
    
    def voyage_itinerary(self, imo, vesselname, vesselcode, voyagestatus, payload=None):
        """Voyage Itinerary API with middleware token"""
        endpoint = "/api/master/middleware/v1/voyageItinerary"
        # if(payload is None):
        #     # Create payload with vessel data
        #     payload = AuthPayloads.voyage_itinerary_payload(imo, vesselname, vesselcode, voyagestatus)
        
        # Log request details
        self.log_request("POST", endpoint, json_data=payload)

        # Log response for debugging
        response = self.client.post(endpoint, json=payload)
        AuthAPI.log_response(response)
        
        return response
