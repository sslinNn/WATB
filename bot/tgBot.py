import asyncio
import logging
import os
import sys
import pandas as pd
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from dotenv import load_dotenv

from weather.getLocaion import getLocationFromCoordinates, getLocationFromCityName
from bot.handlers.weatherHendler import getWather_hendler
from statements.User import User
from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers
import datetime
from tabulate import tabulate




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

router = Router()



#ЧЕ ТО Я НЕ СМОГ В ОТДЕЛЬНЫЙ ФАЙЛИК И ПОТОМ СЮДА, АНЛАК
@dp.message(F.text.lower() == 'в меню')
async def menu(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Настройки'), types.KeyboardButton(text='Какой город у меня указан?'), types.KeyboardButton(text='Ввести секретный код'))
    builder.adjust(2)
    await message.answer(f'Главное меню', reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == 'ввести секретный код')
async def enter_code(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    await message.answer(f'Введите код после /code', reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(Command(commands=['code']))
async def answer_to_code(message: types.Message, state: FSMContext, command: CommandObject):
    if command.args.lower() == 'nhtk' or command.args.lower() == 'нхтк':
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Студент'), types.KeyboardButton(text='Преподаватель'), types.KeyboardButton(text='В меню'))
        builder.adjust(2)
        await message.answer(f'Вы ввели код: {command.args}, вы явно о чем-то знаете! Если вы хотите получать расписание, пожалуйста, скажите кто вы?', reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == 'студент')
async def select_group(message: types.Message):
    df = getScheduleNHTK_groups()
    groups = df['GroupName'].tolist()
    print(len(groups))
    builder = ReplyKeyboardBuilder()
    for i in groups:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    builder.row(types.KeyboardButton(text='В меню'))  # Отдельная строка для "В меню"
    await message.answer(
        "Выберите группу из списка или введите вручную",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.text.lower() == 'преподаватель')
async def select_teacher(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))  # Отдельная строка для "В меню"
    await message.answer(
        "Увы, кнопок нет, но вы можете ввести свою фамилию (например: Иванов. И. И.)",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


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
    print(df_str)
    await message.answer(
        f'<pre>{df_str}</pre>',
        parse_mode='HTML',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command(commands=['weekly_schedule']))
@dp.message(F.text.lower() == 'расписание на неделю')
async def tomorrow_schedule(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    df = get_weekly_schedule_group('09.07.11')
    df_str = df.to_string(index=False)
    print(df_str)
    await message.answer(
        f'<pre>{df_str}</pre>',
        parse_mode='HTML',
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(F.text.lower() == 'ввести вручную')
async def whereIamManually(message: types.Message):
    await message.answer(text='Хорошо, введите ваш город после /city')

@dp.message(Command(commands=['city']))
async def manuallyCity(message: types.Message, state: FSMContext, command: CommandObject):
    if command.args:
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Какой город у меня указан?'), types.KeyboardButton(text='В меню')
        )
        city, country, fixed = getLocationFromCityName(TOKEN=TOKENYA, NAME=str(command.args))
        if fixed:
            await message.answer(f"Установлен город: {city}, страна: {country}",
                             reply_markup=builder.as_markup(resize_keyboard=True))
            await state.update_data({'location': city})
        else:
            await message.answer(f"Вы допустили ошибку, будет выбран город: {city}, страна: {country}",
                             reply_markup=builder.as_markup(resize_keyboard=True))
            await state.update_data({'location': city})
    else:
        await message.answer("Пожалуйста, введите ваш город после /city")



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
