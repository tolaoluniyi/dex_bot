import requests

class DexHandler:
    def __init__(self):
        self.base_url = "https://api.dexscreener.com/latest/dex"

    def get_coins(self):
        """
        Fetches token data from Dexscreener.
        :return: A list of dictionaries containing token data.
        """
        try:
            # Fetch top tokens from Dexscreener
            response = requests.get(f"{self.base_url}/tokens")
            if response.status_code == 200:
                tokens = response.json().get("tokens", [])
                return self._parse_tokens(tokens)
            else:
                print(f"Failed to fetch tokens: {response.text}")
                return []
        except Exception as e:
            print(f"Error fetching tokens: {e}")
            return []

    def _parse_tokens(self, tokens):
        """
        Parses raw token data into a structured format.
        :param tokens: Raw token data from Dexscreener.
        :return: A list of dictionaries with parsed token data.
        """
        parsed_tokens = []
        for token in tokens:
            try:
                parsed_token = {
                    "name": token.get("name", "Unknown"),
                    "symbol": token.get("symbol", "UNKNOWN"),
                    "address": token.get("address", "0x0"),
                    "price": float(token.get("priceUsd", 0)),
                    "volume": float(token.get("volume", {}).get("h24", 0)),
                    "supply": float(token.get("totalSupply", 0)),
                    "dev": token.get("dev", "Unknown"),
                    "chain": token.get("chain", "Unknown")
                }
                parsed_tokens.append(parsed_token)
            except Exception as e:
                print(f"Error parsing token: {e}")
        return parsed_tokens
