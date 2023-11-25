import datetime
import os

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from bot.model.querys import Request
from bot.statements.states import Menu, Secrets, Schedule
from bot.schedule.converting_df_bez_xyini import df_to_png
from bot.schedule.selected_schedule_parser import (
    get_daily_schedule,
    get_weekly_schedule_group,
    get_weekly_schedule_teacher
)
from bot.schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers

from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SecretKB import getScheduleKB
from bot.keyboard.emoji_control import remove_emojis


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def schedulePicker(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    user_id = message.from_user.id
    class_identifier = await Request(request).select_class_in_db(user_id)
    role = await Request(request).select_role_in_db(user_id)
    if remove_emojis(message.text.lower()) == 'расписание на завтра':
        await state.set_state(Schedule.schedule)
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_new = '.'.join(str(tomorrow).split('-')[::-1])
        try:
            df = get_daily_schedule(class_identifier, tomorrow_new)
            photo = df_to_png(df)
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
        except AttributeError as e:
            await message.answer('Кажется завтра нет пар, но это не точно...')
    elif remove_emojis(message.text.lower()) == 'расписание на ...':
        builder = ReplyKeyboardBuilder()
        if role == 'student':
            df = get_weekly_schedule_group(class_identifier)
        else:
            df = get_weekly_schedule_teacher(class_identifier)
        days = [i for i in df['DAY'].unique()]
        for i in days:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(3)
        await state.set_state(Schedule.choice_day)
        await message.answer('Выберите дату', reply_markup=builder.as_markup(resize_keyboard=True))
    elif remove_emojis(message.text.lower()) == 'расписание на сегодня':
        await state.set_state(Schedule.schedule)
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        today = datetime.date.today()
        today = '.'.join(str(today).split('-')[::-1])
        try:
            df = get_daily_schedule(class_identifier, today)
            photo = df_to_png(df)
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
        except AttributeError as e:
            print(e)
            await message.answer('Кажется сегодня нет пар, но это не точно...')
    elif remove_emojis(message.text.lower()) == 'всё доступное расписание':
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        await state.set_state(Schedule.schedule)
        group = await state.get_data()
        try:
            if role == 'student':
                df = get_weekly_schedule_group(class_identifier)
                photo = df_to_png(df)
            else:
                df = get_weekly_schedule_teacher(class_identifier)
                photo = df_to_png(df)
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
        except AttributeError as e:
            await message.answer(text='Что-то пошло не так, попробуйте снова или заново введите /code nhtk')
            print(e)
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB(user_id, request))
    else:
        await message.answer('Не знаю такх ответов!')


@dp.message(Schedule.choice_day)
async def choiceDay(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    class_identifier = Request(request).select_class_in_db(message.from_user.id)
    df = get_daily_schedule(str(class_identifier), str(message.text))
    photo = df_to_png(df)
    await bot.send_photo(chat_id=message.chat.id,
                         photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
    await message.answer('Выберите доступную дату')
