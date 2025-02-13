from dex_handler import DexHandler
from rugcheck import RugCheck
from volume_check import VolumeCheck
from telegram_bot import TelegramBot
from bitget_api import BitgetAPI
from utils import load_config, log_message

class DexBot:
    def __init__(self):
        self.config = load_config("config/config.yaml")
        self.dex_handler = DexHandler()
        self.rugcheck = RugCheck()
        self.volume_check = VolumeCheck()
        self.telegram_bot = TelegramBot(self.config["telegram"]["bot_token"], self.config["telegram"]["chat_id"])
        self.bitget_api = BitgetAPI(
            self.config["bitget"]["api_key"],
            self.config["bitget"]["api_secret"],
            self.config["bitget"]["api_passphrase"]
        )

    def run(self):
        coins = self.dex_handler.get_coins()
        for coin in coins:
            if self._is_coin_valid(coin):
                self._process_coin(coin)

    def _is_coin_valid(self, coin):
        # Check blacklists
        if coin["address"] in self.config["blacklist"]["coins"]:
            return False
        if coin["dev"] in self.config["blacklist"]["devs"]:
            return False

        # Check rugcheck.xyz
        rugcheck_result = self.rugcheck.check_contract(coin["address"])
        if rugcheck_result != "Good":
            return False

        # Check bundled supply
        if coin["supply"] > self.config["filters"]["max_supply_bundled"]:
            return False

        # Check fake volume
        if self.volume_check.is_fake_volume(coin):
            return False

        return True

    def _process_coin(self, coin):
        log_message(f"Processing coin: {coin['name']} ({coin['address']})")
        self.telegram_bot.send_message(f"New coin detected: {coin['name']}")

        # Trade using Bitget API
        symbol = f"{coin['symbol']}USDT"  # Assuming trading against USDT
        balance = self.bitget_api.get_balance("USDT")
        if balance > 10:  # Minimum balance to trade
            amount = balance * 0.1  # Use 10% of balance for each trade
            response = self.bitget_api.place_order(symbol, "buy", amount)
            if response["code"] == "00000":
                self.telegram_bot.send_message(f"Successfully bought {amount} of {coin['name']}")
            else:
                self.telegram_bot.send_message(f"Failed to buy {coin['name']}: {response['msg']}")
