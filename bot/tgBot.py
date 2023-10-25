import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from statements.states import StartWithUser, Menu, Settings

from handlers.StartWithUser import message_handler, yes, location, accepting
from handlers.Menu import menu, menuPicker
from handlers.Settings import changeLocate

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.message.register(message_handler, CommandStart())
    dp.message.register(yes, StartWithUser.yes)
    dp.message.register(location, StartWithUser.location)
    dp.message.register(accepting, StartWithUser.accepting)
    dp.message.register(menu, Menu.menu)
    dp.message.register(menuPicker, Menu.menuPicker)
    dp.message.register(changeLocate, Settings.location)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
