class AuthPayloads:

    @staticmethod
    def login_payload(username, password):
        return {
            "userName": username,
            "password": password
        }
    
    @staticmethod
    def bunker_consumption_vessel_payload(range,limit,favVessel):
        return {
            "range":range,
            "limit":limit,
            "favouriteVessel":favVessel
        }