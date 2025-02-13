import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

class BitgetAPI:
    def __init__(self, api_key, api_secret, api_passphrase):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.base_url = "https://api.bitget.com"

    def _generate_signature(self, message):
        return hmac.new(
            self.api_secret.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def _get_headers(self, method, endpoint, params=None):
        timestamp = str(int(time.time() * 1000))
        message = f"{timestamp}{method}{endpoint}{params if params else ''}"
        signature = self._generate_signature(message)
        return {
            "ACCESS-KEY": self.api_key,
            "ACCESS-SIGN": signature,
            "ACCESS-TIMESTAMP": timestamp,
            "ACCESS-PASSPHRASE": self.api_passphrase,
            "Content-Type": "application/json",
        }

    def place_order(self, symbol, side, amount, price=None):
        endpoint = "/api/spot/v1/trade/orders"
        url = self.base_url + endpoint
        params = {
            "symbol": symbol,
            "side": side,
            "type": "limit" if price else "market",
            "size": amount,
            "price": price,
        }
        headers = self._get_headers("POST", endpoint, urlencode(params))
        response = requests.post(url, json=params, headers=headers)
        return response.json()

    def get_balance(self, coin):
        endpoint = "/api/spot/v1/account/assets"
        url = self.base_url + endpoint
        headers = self._get_headers("GET", endpoint)
        response = requests.get(url, headers=headers)
        for asset in response.json()["data"]:
            if asset["coin"] == coin:
                return float(asset["available"])
        return 0.0
