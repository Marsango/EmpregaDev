import requests
from scrappers.settings import api_key_telegram, channel_id

class TelegramBot:
    def __init__(self) -> None:
        self.__api_key = api_key_telegram
        self.__channel_id = channel_id

    def send_message(self, message: str) -> None:
        params = {
            "chat_id": self.__channel_id,
            "text": message
        }
        response = requests.get(f"https://api.telegram.org/bot{self.__api_key}/sendMessage", params=params)
