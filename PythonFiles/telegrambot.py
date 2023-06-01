from telegram import Bot
import requests
from datetime import datetime

class TelegramBot:
    __TOKEN = "6111372734:AAH-AdTXdJDTX7UDfRqdCFnVck1ewGi4-AM"
    __chat_id = "-1001944555399"
    @staticmethod
    def sendParticulateMessage(location, main_option, changeInfo):  # 현재위치, 사용자가 켜둔 설정, 전과 달라진 정보들 모아둔 list
        str = "/"
        optionDict = main_option.__dict__
        print("Run sendParticulateMessage!!")

        if not changeInfo:
            return
        for info in changeInfo:
            if optionDict[info]:
                if info[-1] == '0':
                    str += '미세먼지 - '
                elif info[-1] == '5':
                    str += '초미세먼지 - '
                else:
                    str += '오존 - '

                str = str + textDict[info][0] + "/"

        sendText = datetime.today().strftime("%p %I:00 - ") + location + str

        data = {"chat_id": TelegramBot.__chat_id, "text": sendText}
        url = f"https://api.telegram.org/bot{TelegramBot.__TOKEN}/sendMessage?"
        res = requests.post(url, json=data)
        # print(res.json())

    @staticmethod
    def makeParticulateToStr(diffList):
        text = ''
        for d in diffList:
            text += textDict[d][0]
        return text

textDict = {
        "beSunny"    : ["맑음", "구름없는 하늘이네요!"],
        "beRainy"    : ["비", "비와요 우산 챙기세요!"],
        "beLighting" : ["번개", "천둥 칠거에요 조심하세요!"],
        "beCloudy"   : ["흐림", "하늘에 구름이 가득할거에요!"],
        # "beFoggy"    : [""],
        # "beClear"    : list(),
        # "beDry"      : list(),
        # "beHumid"    : list(), # 습함
        # "beWindy"    : list(),

        "beGreat_pm10"    : ["좋음", ""],
        "beNormal_pm10"   : ["보통", ""],
        "beBad_pm10"      : ["나쁨", ""],
        "beTooBad_pm10"   : ["매우나쁨", ""],

        "beGreat_pm25"    : ["좋음", ""],
        "beNormal_pm25"   : ["보통", ""],
        "beBad_pm25"      : ["나쁨", ""],
        "beTooBad_pm25"   : ["매우나쁨", ""],

        "beGreat_o3"    : ["좋음", ""],
        "beNormal_o3"   : ["보통", ""],
        "beBad_o3"      : ["나쁨", ""],
        "beTooBad_o3"   : ["매우나쁨", ""],

        "beHot"   : ["급상승", "더워집니다!"],
        "beCold"   : ["급하강", "추워집니다!"],
}

if __name__ == '__main__':
    pass