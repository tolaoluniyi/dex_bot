import requests

class RugCheck:
    def __init__(self):
        self.base_url = "https://rugcheck.xyz/api"

    def check_contract(self, contract_address):
        """
        Checks the contract on rugcheck.xyz and returns the status.
        """
        try:
            response = requests.get(f"{self.base_url}/contracts/{contract_address}")
            if response.status_code == 200:
                data = response.json()
                return data.get("status", "Unknown")
            else:
                print(f"Failed to check contract: {response.text}")
                return "Unknown"
        except Exception as e:
            print(f"Error checking contract: {e}")
            return "Unknown"
