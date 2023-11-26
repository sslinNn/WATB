import os

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather import getWeather
from bot.statements.states import StartWithUser, Menu, Settings
from bot.model.querys import Request

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
from handlers.weatgerDrop import weather_drop

async def notification_sender(request: sqlalchemy.Connection, apscheduler: AsyncIOScheduler):
    time = await Request(request).select_notification_time_from_db_by_id(id_=message.from_user.id)
    print(time)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# scheduler.add_job(weather_drop, trigger='date', run_date=datetime.time(hour=))

if __name__ == '__main__':
    notification_sender(Settings.notification_time)
