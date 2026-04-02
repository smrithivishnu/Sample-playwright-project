import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "usertype": "2"
        })

    def set_token(self, token):
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def get(self, endpoint, headers=None):
        return self.session.get(f"{self.base_url}{endpoint}", headers=headers)

    def post(self, endpoint, json=None, headers=None):
        return self.session.post(f"{self.base_url}{endpoint}", json=json, headers=headers)

    def put(self, endpoint, json=None, headers=None):
        return self.session.put(f"{self.base_url}{endpoint}", json=json, headers=headers)

    def delete(self, endpoint, headers=None):
        return self.session.delete(f"{self.base_url}{endpoint}", headers=headers)