from bs4 import BeautifulSoup as bs
import requests



def GetWeatherInformation():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')

    #위치
    location = soup.find("h2",{"class":"blind"}).text
    #print(location)

    #현재온도
    temperature = soup.find("div",{"class":"temperature_text"}).text.strip()[5:]
    #print(temperature)

    #날씨상태
    weather_state = soup.find("span",{"class":"weather before_slash"}).text
    #print(weather_state)

    return location,temperature,weather_state





if __name__ == '__main__':
    GetWeatherInformation()