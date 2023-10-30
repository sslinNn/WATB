import os
import requests
from dotenv import load_dotenv
from translate import Translator

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def getWeather(locate: str, weather_api_key: str):
    api_url_base = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={locate}&aqi=yes'
    weather_res = requests.get(url=api_url_base)
    condition = weather_res.json()["current"]["condition"]["text"]

    print(weather_res.json())
    return (f'Местное время: {weather_res.json()["location"]["localtime"]} \n'
            f'{weather_res.json()["current"]["temp_f"]}°F \n'
            f'{weather_res.json()["current"]["temp_c"]}°C \n'
            f'Направление ветра: {wind_dir(weather_res.json()["current"]["wind_degree"])}\n'
            f'Ветер: {weather_res.json()["current"]["wind_kph"]} км/ч \n'
            f'{trans(condition)} !!!\n'
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


if __name__ == '__main__':
    print(getWeather(weather_api_key=WEATHER_API_KEY, locate='Новосибирск'))