import os

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from bot.model.querys import Request
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather import getWeather
from bot.statements.states import StartWithUser, Menu


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def weather_drop(message: types.Message, state: FSMContext):
    await state.set_state(StartWithUser.location)
    try:
        location = await state.get_data()
        await message.answer(text=f'{getWeather({location["location"]}, weather_api_key=WEATHER_API_KEY)}')
        await state.set_state(Menu.menuPicker)
    except Exception as ex:
        print(ex)
        await message.answer(text='Я не знаю где вы находитесь!')
