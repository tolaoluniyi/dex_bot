import requests

class TelegramBot:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def send_message(self, message):
        """
        Sends a message to the specified Telegram chat.
        """
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Message sent to Telegram: {message}")
            else:
                print(f"Failed to send message: {response.text}")
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
