from telegram import Bot
import requests
from datetime import datetime
import option

options = option.Option()
class TelegramBot:
    __TOKEN = "6111372734:AAH-AdTXdJDTX7UDfRqdCFnVck1ewGi4-AM"
    __chat_id = "-1001944555399"
    optionDict = options.__dict__
    @staticmethod
    def sendParticulateMessage(location, optionDict):
        str = "/"
        for k, v in optionDict.items():
            if v:
                str = str + textDict[k] + "/"

        sendText = datetime.today().strftime("%p %I:00 - ") + location + str

        data = {"chat_id": TelegramBot.__chat_id, "text": sendText}
        url = f"https://api.telegram.org/bot{TelegramBot.__TOKEN}/sendMessage?"
        res = requests.post(url, json=data)
        # print(res.json())

    @staticmethod
    def makeParticulateToStr():

        pass

textDict = {
        "beRainy"    : list(),
        "beSunny"    : list(),
        "beCloudy"   : list(),
        "beClear"    : list(),
        "beDry"      : list(),
        "beHumid"    : list(), # 습함
        "beFoggy"    : list(),
        "beLighting" : list(),
        "beWindy"    : list(),

        "beGreat"    : "좋음",
        "beNormal"   : "보통",
        "beBad"      : "나쁨",
        "beTooBad"   : "매우나쁨",
}

if __name__ == '__main__':
    # t = TelegramBot()

    o = option.Option()
    o.beGreat = True
    o.beNormal = True
    TelegramBot().sendParticulateMessage('정왕동', o.__dict__)