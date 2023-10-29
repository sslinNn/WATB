import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from schedule.converting_df import df_to_png

from aiogram.types import InputMediaPhoto, FSInputFile

from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers

from statements.states import StartWithUser, Menu, Settings, Secrets

from handlers.StartWithUser import message_handler, yes, location, accepting
from handlers.Menu import menu, menuPicker
from handlers.Settings import changeLocate
from handlers.Secrets import code, nhtk, nhtkGroup, schedulePicker



load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(Command(commands=['tomorrow_schedule']))
@dp.message(F.text.lower() == 'расписание на завтра')
async def tomorrow_schedule(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_new = '.'.join(str(tomorrow).split('-')[::-1])
    df = get_daily_schedule('09.07.11', tomorrow_new)

    df_str = df.to_string(index=False)
    path = df_to_png(df)
    photo = FSInputFile('output/output.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message(Command(commands=['weekly_schedule']))
@dp.message(F.text.lower() == 'расписание на неделю')
async def tomorrow_schedule(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    df = get_weekly_schedule_group('09.07.11')
    df_str = df.to_string(index=False)
    path = df_to_png(df)
    photo = FSInputFile('output/output.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    

async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.message.register(message_handler, CommandStart())
    dp.message.register(yes, StartWithUser.yes)
    dp.message.register(location, StartWithUser.location)
    dp.message.register(accepting, StartWithUser.accepting)
    dp.message.register(menu, Menu.menu)
    dp.message.register(menuPicker, Menu.menuPicker)
    dp.message.register(changeLocate, Settings.location)
    dp.message.register(code, Secrets.code)
    dp.message.register(nhtk, Secrets.nhtk)
    dp.message.register(nhtkGroup, Secrets.nhtkGroup)
    dp.message.register(schedulePicker, Secrets.schedulePicker)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
