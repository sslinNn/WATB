import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
locate = 'Novosibirsk'

api_url_base = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={locate}&aqi=yes'

weather_res = requests.get(url=api_url_base)
# print(weather_res.json())
with open('weatherData.json', 'w') as f:
    json.dump(weather_res.json(), f)
