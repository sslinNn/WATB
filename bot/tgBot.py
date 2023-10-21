import logging
import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def message_handler(message: types.Message):
    await message.reply(f'Привет! Хочешь узнать погоду?')


@dp.message()
async def echo_handler(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('NT, Homie!')


async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
