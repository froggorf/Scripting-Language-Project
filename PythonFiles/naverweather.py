from bs4 import BeautifulSoup as bs
import requests

mainsoup = None

def GetWeatherInformation():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text, 'html.parser')

    global mainsoup
    mainsoup=soup
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

    #GetWeekWeatherForecast(soup)
    # print(f'{location=}, {temperature=}')
    # print(temperature_per_hour)
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

def GetWeekWeatherForecast():
    week_weathers_from_naver = mainsoup.findAll("span", {"class":"weather_inner"})
    weather_state_am = list()
    weather_state_pm = list()
    rain_fall_am = list()
    rain_fall_pm = list()
    for index, data in enumerate(week_weathers_from_naver):
        ws = data.find("span",{"class":"blind"}).text
        if index % 2 == 0 :
            weather_state_am.append(ws)
            rain_fall_am.append(data.find("span", {"class": "rainfall"}).text)
        else:
            weather_state_pm.append(ws)
            rain_fall_pm.append(data.find("span", {"class": "rainfall"}).text)




    week_data =mainsoup.findAll("div",{"class":"cell_date"})
    all_week = list()
    for index,data in enumerate(week_data):
        all_week.append((data.find("strong",{"class":"day"}).text, data.find("span",{"class":"date"}).text[:-1]))
    #print(all_week)
    #print(weather_state_am)
    #print(weather_state_pm)
    #print(rain_fall_am)
    #print(rain_fall_pm)

    max_temp_data = mainsoup.findAll("span",{"class":"highest"})
    min_temp_data = mainsoup.findAll("span", {"class": "lowest"})

    max_temp = list()
    min_temp = list()
    for data in max_temp_data:
        max_temp.append(data.text[4:])
    for data in min_temp_data:
        min_temp.append(data.text[4:])

    return all_week, weather_state_am, weather_state_pm, rain_fall_am, rain_fall_pm, max_temp, min_temp








if __name__ == '__main__':
    GetWeatherInformation()
    GetWeekWeatherForecast()
