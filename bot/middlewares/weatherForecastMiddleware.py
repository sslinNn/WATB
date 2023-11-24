from typing import Callable, Awaitable, Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from bot.model.querys import select_location_from_db
from weather.graphs import weather_graph
from weather.getWeather import parse_api
from bot.keyboard.emoji_control import remove_emojis
from dotenv import load_dotenv
import os


class weather_forecast(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        if remove_emojis(event.text).lower() == 'меню':
            load_dotenv()
            self.WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
            state = data.get('state')
            state_data = await state.get_data()
            location = state_data.get('location', None)
            df, sun, date = parse_api(location, self.WEATHER_API_KEY)
            photo = weather_graph(df, sun, date, location)
            data['photo'] = photo
            return await handler(event, data)