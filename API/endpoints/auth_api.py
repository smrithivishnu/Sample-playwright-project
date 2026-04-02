from API.clients.api_client import APIClient
from API.payloads.auth_payloads import AuthPayloads
import allure
import json

class AuthAPI:

    def __init__(self, base_url):
        self.client = APIClient(base_url)

    def log_response(response):
        print("\n--- API RESPONSE ---")
        print("Status:", response.status_code)
        try:
            print(json.dumps(response.json(), indent=4))
            allure.attach(
            json.dumps(response.json(), indent=4),
            name="API Response",
            attachment_type=allure.attachment_type.JSON
            )
        except:
            print(response.text)

    def login(self, username, password):
        payload = AuthPayloads.login_payload(username, password)
        return self.client.post("/auth/v1/login", json=payload)
    
    def bunker_consumption_vessel(self, range, limit, favVessel):
        payload = AuthPayloads.bunker_consumption_vessel_payload(range, limit, favVessel)
        return self.client.post("/monitor/dashboard/v1/bunker-consumption-vessel", json=payload)
    
    def inventory_rob_summary(self):
        return self.client.get("/api/inventory/dashboard/v1/rob/summary/2026/false")

    