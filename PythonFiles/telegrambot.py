from telegram import Bot
import requests
from datetime import datetime

class TelegramBot:
    def __init__(self):
        pass

    def sendMessage(self):
        __TOKEN = "6111372734:AAH-AdTXdJDTX7UDfRqdCFnVck1ewGi4-AM"
        __chat_id = "-1001944555399"


        sendText = datetime.today().strftime("%p %I:00 - ")

        data = {"chat_id": __chat_id, "text": sendText}
        url = f"https://api.telegram.org/bot{__TOKEN}/sendMessage?"
        res = requests.post(url, json=data)
        print(res.json())

if __name__ == '__main__':
    t = TelegramBot()
    t.sendMessage()