import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command(commands='help'))
async def help_command(message: types.Message):
    await message.answer('Вот справка по боту: ')

@dp.message(CommandStart())
async def message_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Да!'),
    )
    await message.answer(f'Привет! Хочешь узнать погоду?', reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == 'да!')
async def yes(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='Отправить геолокацию', request_location=True),
    )
    await message.answer('Тогда поделись со мной своей геолокацией, пожалуйста!',
                         reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.location)
async def handle_location(message: types.Message):
    lon = message.location.longitude
    lat = message.location.latitude
    print(f'longitude {lon} | latitude {lat}')



async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
