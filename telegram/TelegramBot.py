import requests
from TELEGRAM_BOT_INFO import api_key, channel_id
class TelegramBot:
    def __init__(self) -> None:
        self.__api_key = api_key
        self.__channel_id = channel_id

    def send_message(self, message: str) -> None:
        response = requests.get(f"https://api.telegram.org/bot{self.__api_key}/sendMessage?chat_id={self.__channel_id}&text={message}")
        print(response)
        print(response.text)