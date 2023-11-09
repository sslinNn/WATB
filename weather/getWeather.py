import os
import subprocess
import pandas as pd
import requests
from dotenv import load_dotenv
from translate import Translator
import datetime
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
import json


load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def getWeather(locate: str, weather_api_key: str):
    api_url_base = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={locate}&lang=ru&aqi=yes'
    weather_res = requests.get(url=api_url_base)
    condition = weather_res.json()["current"]["condition"]["text"]
    return (f'Местное время: {weather_res.json()["location"]["localtime"]} \n'
            f'{weather_res.json()["current"]["temp_f"]}°F \n'
            f'{weather_res.json()["current"]["temp_c"]}°C \n'
            f'Направление ветра: {wind_dir(weather_res.json()["current"]["wind_degree"])}\n'
            f'Ветер: {weather_res.json()["current"]["wind_kph"]} км/ч \n'
            f'{condition}!!!\n'
            f'Ощущается как: {round(feel_like(weather_res.json()["current"]["temp_c"], weather_res.json()["current"]["wind_kph"]))}°C (Посчитано вручную) \n'
            f'Ощущается как: {weather_res.json()["current"]["feelslike_c"]}°C (Дано в API) \n')


def wind_dir(wind):
    wind_directions = {
        0: 'Север',
        45: 'Северо-восток',
        90: 'Восток',
        135: 'Юго-восток',
        180: 'Юг',
        225: 'Юго-запад',
        270: 'Запад',
        315: 'Северо-запад'
    }
    wind_degree = wind
    wind_dir_code = None
    for degrees, code in wind_directions.items():
        if wind_degree >= degrees:
            wind_dir_code = code
        else:
            break
    return wind_dir_code


def trans(input_word):
    translator = Translator(from_lang='English', to_lang='Russian')
    result = translator.translate(input_word)
    return result


def feel_like(temp_c, wind_kph):
    return 13.12 + 0.6215 * temp_c - 11.37 * wind_kph**0.16 + 0.3965 * temp_c * wind_kph**0.16


def parse_api(locate: str, weather_api_key: str):
    api_url_forecast = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={locate}&lang=ru&aqi=yes'
    weather_res = requests.get(url=api_url_forecast)
    date = convert_parse_date_to_normal_date(weather_res.json()["forecast"]["forecastday"][0]['date'])
    per_hour = weather_res.json()["forecast"]["forecastday"][0]['hour']
    hour = []
    temp_c = []
    condition = []
    wind = []
    img_condition = []
    for i in per_hour:
        hour.append(i['time'].split(' ')[1])
        temp_c.append(i['temp_c'])
        condition.append(i['condition']['text'])
        wind.append(i['wind_kph'])
        img_condition.append(f"https:{i['condition']['icon']}")
        pass
    df = pd.DataFrame({'Hour': hour, 'Temp_C': temp_c, 'Condition': condition, 'Wind': wind, 'Icon': img_condition})
    df = df.set_index('Hour').T
    return df, [weather_res.json()["forecast"]["forecastday"][0]['astro']['sunrise'], weather_res.json()["forecast"]["forecastday"][0]['astro']['sunset']]


def getWeatherForecast(locate: str, weather_api_key: str):
    api_url_forecast = f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={locate}&aqi=yes'
    weather_res = requests.get(url=api_url_forecast)
    date = convert_parse_date_to_normal_date(weather_res.json()["forecast"]["forecastday"][0]['date'])
    return (
        f'Прогноз погоды на {date[2]} {date[1]}\n'
        f'Днем в среднем: {weather_res.json()["forecast"]["forecastday"][0]["day"]["avgtemp_c"]}°C ({weather_res.json()["forecast"]["forecastday"][0]["day"]["avgtemp_f"]}°F)'
    )


def convert_parse_date_to_normal_date(date):
    months = {
        "января": '01',
        "февраля": '02',
        "марта": '03',
        "апреля": '04',
        "мая": '05',
        "июня": '06',
        "июля": '07',
        "августа": '08',
        "сентября": '09',
        "октября": '10',
        "ноября": '11',
        "декабря": '12'
    }
    parts = date.split("-")
    for k, v in months.items():
        if v == parts[1]:
            parts[1] = k
    return parts


# def download_json(locate: str, weather_api_key: str):
#     json_url = f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={locate}&lang=ru&aqi=yes"
#     response = requests.get(json_url)
#     data = response.json()
#     with open("input.json", "w") as file:
#         json.dump(data["forecast"]["forecastday"][0]['hour'], file)
#
#
# def retrieve_processed_data():
#     subprocess.run(["go", "run", "parse_weather_api.go"])
#     with open('output.json', 'r') as file:
#         data = json.load(file)
#     return data


# def forecast_weather(locate: str, weather_api_key: str):
#     download_json(locate, weather_api_key)
#     dic = retrieve_processed_data()
#     df = pd.DataFrame(data=[v for k, v in dic.items() if k != 'Hour'], columns=dic['Hour'])
#     return df


if __name__ == '__main__':
    # print(parse_api(weather_api_key=WEATHER_API_KEY, locate='Новосибирск'))
    print(parse_api(weather_api_key=WEATHER_API_KEY, locate='Новосиб'))
    print(datetime.datetime.now())