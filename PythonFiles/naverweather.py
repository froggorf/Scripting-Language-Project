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
    #<div class="forecast_wrap _selectable_tab">
    temperature_per_hour = GetTemperaturePer2Hour(soup.find("div",{"class":"forecast_wrap _selectable_tab"}))
    return location,temperature,weather_state, temperature_per_hour

def GetTemperaturePer2Hour(soup):
    time = soup.findAll("dt",{"class":"time"})
    weather_state = soup.findAll("span",{"class":"blind"})
    degree = soup.findAll("span", {"class": "num"})
    all_time = list()
    all_weather_state = list()
    all_degree = list()
    for i in range(48):
        all_time.append(time[i].text)
        all_weather_state.append(weather_state[i].text)
        all_degree.append(int(degree[i].text[:-1]))




    return all_time,all_weather_state,all_degree









if __name__ == '__main__':
    GetWeatherInformation()