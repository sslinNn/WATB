import os
import requests
import json
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('YANDEX_API_KEY')


def getLocationFromCoordinates(TOKEN: str, latitude: float, longitude: float):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={longitude},{latitude}&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    return location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][4]['name']

def getLocationFromCityName(TOKEN: str, NAME: str):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={NAME}&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    geo = location_res['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']
    suggest = geo.get('suggest', None)
    country_name = location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][0]['name']
    if suggest:
        return re.sub(r'<[^>]+>', '', suggest).title(), country_name, False
    else:
        return geo['request'].title(), country_name, True








# with open('locationData.json', 'w', encoding='utf8') as f:
#     json.dump(location_res.json(), f, ensure_ascii=False)
if __name__ == '__main__':
    print(getLocationFromCityName(TOKEN=TOKEN, NAME='масква'))
