import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('YANDEX_API_KEY')


def getLocationFromCoordinates(TOKEN: str, latitude: float, longitude: float):
    api_url_base = f'https://geocode-maps.yandex.ru/1.x/?apikey={TOKEN}&geocode={longitude},{latitude}&format=json'
    response = requests.get(url=api_url_base).text
    location_res = json.loads(response)
    return location_res['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['Components'][4]['name']

# with open('locationData.json', 'w', encoding='utf8') as f:
#     json.dump(location_res.json(), f, ensure_ascii=False)
# if __name__ == '__main__':
#     print(getLocationFromCoordinates(TOKEN=TOKEN, latitude=latitude, longitude=longitude))
