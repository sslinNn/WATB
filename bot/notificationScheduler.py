import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather import getWeather
from bot.statements.states import StartWithUser, Menu, Settings

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, time
from handlers.weatgerDrop import weather_drop

async def notification_sender(state: FSMContext):
    data = await state.get_data()
    time = data['notification_time']
    print(time)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
# scheduler.add_job(weather_drop, trigger='date', run_date=datetime.time(hour=))

if __name__ == '__main__':
    notification_sender(Settings.notification_time)
