import datetime
import os
import re

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from bot.model.querys import Request
from bot.statements.states import Menu, Secrets

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


async def nhtk(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    user_id = message.from_user.id
    if remove_emojis(message.text.lower()) == 'студент':
        # await state.clear()
        await Request(request).insert_role_in_db(user_id, 'student')
        await state.set_state(Secrets.nhtkGroup)
        df = getScheduleNHTK_groups()
        groups = df['GroupName'].tolist()
        print(len(groups))
        builder = ReplyKeyboardBuilder()
        for i in groups:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(4)
        builder.row(types.KeyboardButton(text='Меню'))
        await message.answer(
            "Выберите группу из списка или введите вручную",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif remove_emojis(message.text.lower()) == 'преподаватель':
        await Request(request).insert_role_in_db(user_id, 'teacher')
        await state.set_state(Secrets.nhtkTeacher)
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        await message.answer(
            "Увы, кнопок нет, но вы можете ввести свою фамилию (например: Иванов. И. И.)",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB(user_id, request))
    else:
        await message.answer('Такого варианта ответа нет!')


async def nhtkGroup(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
    patternInMessage = re.findall(pattern, message.text)
    user_id = message.from_user.id
    if message.text in patternInMessage:
        await Request(request).insert_group_in_db(user_id, message.text)
        await state.set_state(Secrets.schedulePicker)
        await state.update_data({'group': message.text})
        group = await state.get_data()
        await state.set_state(Menu.menuPicker)
        await message.answer(
            f'Успешно! Ваша группа: {group["group"]} ', reply_markup=getMenuKB(user_id, request)
        )
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB(user_id, request))
    else:
        await message.answer('ЧТо?')


async def nhtkTeacher(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    teacher = message.text
    df = getScheduleNHTK_teachers()
    user_id = message.from_user.id
    if df['Name'].isin([teacher]).any():
        await Request(request).insert_group_in_db(user_id, message.text)
        await state.set_state(Secrets.schedulePicker)
        await state.update_data({'group': teacher})
        group = await state.get_data()
        await state.set_state(Menu.menuPicker)
        await message.answer(
            f'{group["group"]}, успешно!',
            reply_markup=getMenuKB(user_id, request)
        )
    else:
        await message.answer('Попробуйте снова')
    if remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB(user_id, request))
