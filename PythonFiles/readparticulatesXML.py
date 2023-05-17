# 미세먼지 정보읽기
# 지역미세먼지정보적기

# 텔레그램
# 지역설정하기
# 알림설정

# 인증키 Encoding: LUz3gX6MucCzt3GEJeLI2p1uffZns9cE5YlhQOeNHhZ8Fki40iLenLr8Uz21YPvzHHPlXYmIxhlf9%2F3a0d1Qow%3D%3D
# 인증키 Decoding: LUz3gX6MucCzt3GEJeLI2p1uffZns9cE5YlhQOeNHhZ8Fki40iLenLr8Uz21YPvzHHPlXYmIxhlf9/3a0d1Qow==

# Python3 샘플 코드 #

import requests
import xml.etree.ElementTree as ET

class Particulates:
    def __init__(self):
        self.numOfRows = '100'
        self.pageNo = '1'
        self.params = {
            'serviceKey': 'LUz3gX6MucCzt3GEJeLI2p1uffZns9cE5YlhQOeNHhZ8Fki40iLenLr8Uz21YPvzHHPlXYmIxhlf9/3a0d1Qow==',
            'returnType': 'xml', 'numOfRows': self.numOfRows, 'pageNo': self.pageNo }

        self.root = None
        self.items = None
        self.particulates = []

    def getRoot(self):
        return self.root

    def getItem(self, str):
        return self.particulates[str]

    def setParamsUseStationName(self, stationName):
        self.params['stationName'] = stationName



# 대기질 예보통보 조회
class MinuDustFrcstDspth(Particulates):
    def __init__(self):
        super().__init__()
        self.url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustFrcstDspth'
        self.params['searchDate'] = '2023-05-13'
        self.params['InformCode'] = 'PM10'

        self.setNewResponse()

    def setNewResponse(self):
        response = requests.get(self.url, params=self.params)
        self.root = ET.fromstring(response.text)
        self.items = self.root.findall(".//item")
        for item in self.items:
            particulate = {
                "resultCode": item.findtext("resultCode"),
                "resultMsg": item.findtext("resultMsg"),
                "numOfRows": item.findtext("numOfRows"),
                "pageNo": item.findtext("pageNo"),
                "totalCount": item.findtext("totalCount"),

                "informCode": item.findtext("informCode"),
                "informOverall": item.findtext("informOverall"),
                "informCause": item.findtext("informCause"),
                "informGrade": item.findtext("informGrade"),
                "informData": item.findtext("informData"),

                "items": item.findtext("items"),
                "dataTime": item.findtext("dataTime"),
                "actionKnack": item.findtext("actionKnack"),

                "imageUrl1": item.findtext("imageUrl1"),
                "imageUrl2": item.findtext("imageUrl2"),
                "imageUrl3": item.findtext("imageUrl3"),
                "imageUrl4": item.findtext("imageUrl4"),
                "imageUrl5": item.findtext("imageUrl5"),
                "imageUrl6": item.findtext("imageUrl6"),
                "imageUrl7": item.findtext("imageUrl7"),
                "imageUrl8": item.findtext("imageUrl8"),
                "imageUrl9": item.findtext("imageUrl9"),
            }
            self.particulates.append((particulate))
        print("대기질 예보통보 조회 class 생성")

# 초미세먼지 주간예보 조회
class MinuDustWeekFrcstDspth(Particulates):
    def __init__(self):
        super().__init__()
        self.url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMinuDustWeekFrcstDspth'
        self.params['searchDate'] = '2023-05-13'

        self.setNewResponse()

    def setNewResponse(self):
        response = requests.get(self.url, params=self.params)
        self.root = ET.fromstring(response.text)
        self.items = self.root.findall(".//item")
        for item in self.items:
            particulate = {
                "resultCode": item.findtext("resultCode"),
                "resultMsg": item.findtext("resultMsg"),
                "numOfRows": item.findtext("numOfRows"),
                "pageNo": item.findtext("pageNo"),
                "totalCount": item.findtext("totalCount"),

                "frcstOneCn": item.findtext("frcstOneCn"),
                "frcstTwoCn": item.findtext("frcstTwoCn"),
                "frcstThreeCn": item.findtext("frcstThreeCn"),
                "frcstFourCn": item.findtext("frcstFourCn"),

                "presnatnDT": item.findtext("presnatnDT"),

                "frcstOneDt": item.findtext("frcstOneDt"),
                "frcstTwoDt": item.findtext("frcstTwoDt"),
                "frcstThreeDt": item.findtext("frcstThreeDt"),
                "frcstFourDt": item.findtext("frcstFourDt"),
            }
            self.particulates.append((particulate))
        print("대기질 예보통보 조회 class 생성")

# 측정소별 실시간 측정정보 조회
class MsrstnAcctoRltmMesureDnsty(Particulates):
    def __init__(self):
        super().__init__()
        self.url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/' \
                   'getMsrstnAcctoRltmMesureDnsty'
        self.params['stationName'] = '정왕동'
        self.params['dataTerm'] = 'DAILY'
        self.params['ver'] = '1.4'
        self.setNewResponse()

    def setNewResponse(self):
        response = requests.get(self.url, params=self.params)
        self.root = ET.fromstring(response.text)
        self.items = self.root.findall(".//item")
        for item in self.items:
            particulate = {
                "resultCode": item.findtext("resultCode"),
                "resultMsg": item.findtext("resultMsg"),
                "numOfRows": item.findtext("numOfRows"),
                "pageNo": item.findtext("pageNo"),
                "totalCount": item.findtext("totalCount"),
                "items": item.findtext("items"),

                "pm10Value": item.findtext("pm10Value"),
                "pm10Grade": item.findtext("pm10Grade"),
                "pm10Value24": item.findtext("pm10Value24"),
                "pm10Grade1h": item.findtext("pm10Grade1h"),
                "pm10Flag": item.findtext("pm10Flag"),

                "pm25Value": item.findtext("pm25Value"),
                "pm25Grade": item.findtext("pm25Grade"),
                "pm25Value24": item.findtext("pm25Value24"),
                "pm25Grade1h": item.findtext("pm25Grade1h"),
                "pm25Flag": item.findtext("pm25Flag"),

                "khaiValue": item.findtext("khaiValue"),
                "khaiGrade": item.findtext("khaiGrade"),

                "no2Value": item.findtext("no2Value"),
                "no2Grade": item.findtext("no2Grade"),
                "no2Flag": item.findtext("no2Flag"),

                "so2Value": item.findtext("so2Value"),
                "so2Grade": item.findtext("so2Grade"),
                "so2Flag": item.findtext("so2Flag"),

                "o3Value": item.findtext("o3Value"),
                "o3Grade": item.findtext("o3Grade"),
                "o3Flag": item.findtext("o3Flag"),

                "stationName": item.findtext("stationName"),
                "stationCode": item.findtext("stationCode"),

                "coValue": item.findtext("coValue"),
                "coFlag": item.findtext("coFlag"),
                "coGrade": item.findtext("coGrade"),

                "dataTime": item.findtext("dataTime"),
            }
            self.particulates.append((particulate))
        print("측정소별 실시간 측정정보 조회 class 생성")

# 통합대기환경지수 나쁨 이상 측정소 목록조회
class UnityAirEnvrnIdexSnstiveAboveMsrstnList(Particulates):
    def __init__(self):
        super().__init__()
        self.url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/' \
                   'getUnityAirEnvrnIdexSnstiveAboveMsrstnList'

        self.setNewResponse()

    def setNewResponse(self):
        response = requests.get(self.url, params=self.params)
        self.root = ET.fromstring(response.text)
        self.items = self.root.findall(".//item")
        for item in self.items:
            particulate = {
                "resultCode": item.findtext("resultCode"),
                "resultMsg": item.findtext("resultMsg"),
                "numOfRows": item.findtext("numOfRows"),
                "pageNo": item.findtext("pageNo"),
                "totalCount": item.findtext("totalCount"),

                "items": item.findtext("items"),
                "stationName": item.findtext("stationName"),
                "addr": item.findtext("addr"),
            }
            self.particulates.append((particulate))
        print("통합대기환경지수 나쁨 이상 측정소 목록 조회 class 생성")

# 시도별 실시간 측정정보 조회
class CtprvnRltmMesureDnsty(Particulates):
    def __init__(self):
        super().__init__()
        self.url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/' \
                   'getCtprvnRltmMesureDnsty'
        self.params['sidoName'] = '서울'
        self.params['ver'] = '1.4'
        self.setNewResponse()

    def setNewResponse(self):
        response = requests.get(self.url, params=self.params)
        self.root = ET.fromstring(response.text)
        self.items = self.root.findall(".//item")
        for item in self.items:
            particulate = {
                "resultCode": item.findtext("resultCode"),
                "resultMsg": item.findtext("resultMsg"),
                "numOfRows": item.findtext("numOfRows"),
                "pageNo": item.findtext("pageNo"),
                "totalCount": item.findtext("totalCount"),
                "items": item.findtext("items"),

                "pm10Value": item.findtext("pm10Value"),
                "pm10Grade": item.findtext("pm10Grade"),
                "pm10Value24": item.findtext("pm10Value24"),
                "pm10Grade1h": item.findtext("pm10Grade1h"),
                "pm10Flag": item.findtext("pm10Flag"),

                "pm25Value": item.findtext("pm25Value"),
                "pm25Grade": item.findtext("pm25Grade"),
                "pm25Value24": item.findtext("pm25Value24"),
                "pm25Grade1h": item.findtext("pm25Grade1h"),
                "pm25Flag": item.findtext("pm25Flag"),

                "khaiValue": item.findtext("khaiValue"),
                "khaiGrade": item.findtext("khaiGrade"),

                "no2Value": item.findtext("no2Value"),
                "no2Grade": item.findtext("no2Grade"),
                "no2Flag": item.findtext("no2Flag"),

                "so2Value": item.findtext("so2Value"),
                "so2Grade": item.findtext("so2Grade"),
                "so2Flag": item.findtext("so2Flag"),

                "o3Value": item.findtext("o3Value"),
                "o3Grade": item.findtext("o3Grade"),
                "o3Flag": item.findtext("o3Flag"),

                "stationName": item.findtext("stationName"),
                "stationCode": item.findtext("stationCode"),

                "coValue": item.findtext("coValue"),
                "coFlag": item.findtext("coFlag"),
                "coGrade": item.findtext("coGrade"),

                "dataTime": item.findtext("dataTime"),
            }

            self.particulates.append((particulate))
        print("통합대기환경지수 나쁨 이상 측정소 목록 조회 class 생성")

if __name__ == "__main__":
    parti = MsrstnAcctoRltmMesureDnsty()




# print(response.text)
# <response>
#     <header>
#         <resultCode>00</resultCode>
#         <resultMsg>NORMAL_CODE</resultMsg>
#     </header>
#     <body>
#         <items>
#             <item>
#                 <pm25Grade1h>2</pm25Grade1h>
#                 <pm10Value24>44</pm10Value24>
#                 <so2Value>0.004</so2Value>
#                 <pm10Grade1h>2</pm10Grade1h>
#                 <o3Grade>2</o3Grade>
#                 <pm10Value>35</pm10Value>
#                 <pm25Flag/>
#                 <khaiGrade>2</khaiGrade>
#                 <pm25Value>19</pm25Value>
#                 <no2Flag/>
#                 <mangName>도시대기</mangName>
#                 <stationName>종로구</stationName>
#                 <no2Value>0.009</no2Value>
#                 <so2Grade>1</so2Grade>
#                 <stationCode>111123</stationCode>
#                 <coFlag/>
#                 <khaiValue>96</khaiValue>
#                 <coValue>0.4</coValue>
#                 <pm10Flag/>
#                 <no2Grade>1</no2Grade>
#                 <pm25Value24>23</pm25Value24>
#                 <o3Flag/>
#                 <pm25Grade>2</pm25Grade>
#                 <so2Flag/>
#                 <coGrade>1</coGrade>
#                 <dataTime>2023-05-13 15:00</dataTime>
#                 <pm10Grade>2</pm10Grade>
#                 <o3Value>0.085</o3Value>
#             </item>