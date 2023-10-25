import os
import logging
from aiogram import Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather.getWeather import getWeather


load_dotenv()
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
dp = Dispatcher()

@dp.message(Command(commands=['weather']))
async def getWather_hendler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await message.answer(text=f'{getWeather(locate=data["location"], weather_api_key=WEATHER_API_KEY)}')
    except Exception as ex:
        logging.exception(ex)
        await message.answer(text='Я не знаю где вы находитесь!')
