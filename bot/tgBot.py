import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from statements.states import StartWithUser, Menu, Settings, Secrets

from handlers.StartWithUser import message_handler, yes, location, accepting, location_by_number
from handlers.Menu import menu, menuPicker
from handlers.Settings import changeLocate, set_notification_time
from handlers.Secrets import code, nhtk, nhtkGroup, schedulePicker


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
    dp.message.register(changeLocate, Settings.settingPicker)
    dp.message.register(set_notification_time, Settings.notification_time)
    dp.message.register(code, Secrets.code)
    dp.message.register(nhtk, Secrets.nhtk)
    dp.message.register(nhtkGroup, Secrets.nhtkGroup)
    dp.message.register(schedulePicker, Secrets.schedulePicker)
    dp.message.register(location_by_number, StartWithUser.numbers)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
