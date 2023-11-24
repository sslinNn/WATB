import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from model.connection import get_connetion_with_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from statements.states import StartWithUser, Menu, Settings, Secrets, Schedule
from aiogram.filters import Command, CommandStart
from handlers.StartWithUser import message_handler, yes, location, accepting, location_by_number
from handlers.Menu import (menu, menuPicker, secret_code,
                           available_schedule_pdf, available_schedule_xlsx, daily_schedule)
from handlers.weatger_drop import weather_drop
from middlewares.dbmiddleware import DBSession
from handlers.Settings import changeLocate, set_notification_time
from handlers.Secrets import nhtk, nhtkGroup, nhtkTeacher
from handlers.Schedule import schedulePicker, choiceDay, choice_group_and_day

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# scheduler.add_job(weather_drop, trigger='date', run_date=)
engine = get_connetion_with_db()


async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.update.middleware.register(DBSession(engine))
    dp.message.register(message_handler, CommandStart())
    dp.message.register(secret_code, Command('code'))
    dp.message.register(available_schedule_pdf, Command('available_schedule_pdf'))
    dp.message.register(available_schedule_xlsx, Command('available_schedule_xlsx'))
    dp.message.register(daily_schedule, Command('daily_schedule'))
    dp.message.register(yes, StartWithUser.yes)
    dp.message.register(location, StartWithUser.location)
    dp.message.register(accepting, StartWithUser.accepting)
    dp.message.register(menu, Menu.menu)
    dp.message.register(menuPicker, Menu.menuPicker)
    dp.message.register(changeLocate, Settings.settingPicker)
    dp.message.register(set_notification_time, Settings.notification_time)
    dp.message.register(nhtk, Secrets.nhtk)
    dp.message.register(nhtkGroup, Secrets.nhtkGroup)
    dp.message.register(nhtkTeacher, Secrets.nhtkTeacher)
    dp.message.register(schedulePicker, Schedule.schedule)
    dp.message.register(choiceDay, Schedule.choice_day)
    dp.message.register(choice_group_and_day, Schedule.choice_group_and_day)
    dp.message.register(location_by_number, StartWithUser.numbers)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
