from telegram import Bot
import requests
from datetime import datetime
import option


class TelegramBot:
    __TOKEN = "6111372734:AAH-AdTXdJDTX7UDfRqdCFnVck1ewGi4-AM"
    __chat_id = "-1001944555399"
    @staticmethod
    def sendParticulateMessage(location, optionDict):
        str = "/"
        for k, v in optionDict.items():
            if v:
                str = str + k + "/"

        sendText = datetime.today().strftime("%p %I:00 - ") + location + str

        data = {"chat_id": TelegramBot.__chat_id, "text": sendText}
        url = f"https://api.telegram.org/bot{TelegramBot.__TOKEN}/sendMessage?"
        res = requests.post(url, json=data)
        # print(res.json())

    @staticmethod
    def makeParticulateToStr():

        pass


if __name__ == '__main__':
    # t = TelegramBot()
    o = option.Option()
    o.beGreat = True
    o.beDry = True
    TelegramBot().sendParticulateMessage('정왕동', o.__dict__)