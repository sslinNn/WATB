import os
import requests
import json
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('YANDEX_API_KEY')
TOKEN_MAP = os.getenv('YANDEX_API_KEY_MAP')


def getLocationFromCoordinates(TOKEN: str, latitude: float, longitude: float):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={longitude},{latitude}&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    return location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['Components'][4]['name']


def getLocationFromCityName(TOKEN: str, NAME: str):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={NAME}&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    coincidences = [i['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'] for i in location_res['response']['GeoObjectCollection']['featureMember']]
    cords = location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
    geo = location_res['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']
    suggest = geo.get('suggest', None)
    country_name = location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['Components'][0]['name']
    if suggest:
        return re.sub(r'<[^>]+>', '', suggest).title(), country_name, True, cords, coincidences
    else:
        return geo['request'].title(), country_name, False, cords, coincidences


def get_location_from_city_name(TOKEN: str, NAME: str):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={NAME}&kind=locality&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    coincidences = [i['GeoObject']['metaDataProperty']['GeocoderMetaData']['text'] for i in
                    location_res['response']['GeoObjectCollection']['featureMember']
                    if i['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] != 'hydro']
    cords = [i['GeoObject']['Point']['pos'].split(' ') for i in
             location_res['response']['GeoObjectCollection']['featureMember']
             if i['GeoObject']['metaDataProperty']['GeocoderMetaData']['kind'] != 'hydro']
    return coincidences, cords


def get_location_photo(token: str, lat, long):
    api_url = (f'https://static-maps.yandex.ru/v1?lang=ru_RU&ll={lat},{long}&spn=0.5,0.5&apikey={token}')
    response = requests.get(url=api_url).content
    return response

# with open('locationData.json', 'w', encoding='utf8') as f:
#     json.dump(location_res.json(), f, ensure_ascii=False)


if __name__ == '__main__':
    a, b = get_location_from_city_name(TOKEN, 'Москва')
    print(a)
    print(b)
