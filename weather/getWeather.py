import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


def getWeather(locate: str, weather_api_key: str):
    api_url_base = f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={locate}&aqi=yes'
    weather_res = requests.get(url=api_url_base)
    return (f'Местное время: {weather_res.json()["location"]["localtime"]} \n'
            f'{weather_res.json()["current"]["temp_f"]}°F \n'
            f'{weather_res.json()["current"]["temp_c"]}°C \n')


if __name__ == '__main__':
    print(getWeather(weather_api_key=WEATHER_API_KEY, locate='Новосибирск'))
