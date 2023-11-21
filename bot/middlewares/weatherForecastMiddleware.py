from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from bot.model.querys import select_location_from_db
from weather.graphs import weather_graph
from weather.getWeather import parse_api
from dotenv import load_dotenv
import os


class weather_forecast(BaseMiddleware):
    def __int__(self, ID):
        super().__init__()
        self.id_ = ID
        load_dotenv()
        self.WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]],
                       Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        self.location = select_location_from_db(self.id_)
        df, sun, date = parse_api(data['location'], self.WEATHER_API_KEY)
        photo_content = weather_graph(df, sun, date, data['location'])
        