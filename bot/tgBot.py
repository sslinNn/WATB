import asyncio
import logging
import os
import sys
import pandas as pd
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandObject
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather.getLocaion import getLocationFromCoordinates, getLocationFromCityName
from bot.handlers.weatherHendler import getWather_hendler
from statements.User import User
from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers
import datetime
from tabulate import tabulate





load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()


@dp.message(CommandStart())
async def message_handler(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Да!'), )
    await message.answer(f'Привет! Хочешь узнать погоду?', reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == 'да!')
async def yes(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Отправить геолокацию', request_location=True))
    await state.set_state(User.location)
    await message.answer('Тогда поделись со мной своей геолокацией, пожалуйста!',
                         reply_markup=builder.as_markup(resize_keyboard=True))


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


@dp.message(F.location)
async def handle_location(message: types.Message, state: FSMContext):
    lon = message.location.longitude
    lat = message.location.latitude
    builder = ReplyKeyboardBuilder()
    builder.row(
     types.KeyboardButton(text='Да'),
        types.KeyboardButton(text='Нет')
    )
    userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
    await state.set_state(User.location)
    await state.update_data({'location': userLocation})
    await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower() == 'да')
async def whereIam(messaage: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await messaage.answer(text=f'{data["location"]}')
    except KeyError:
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Отправить геолокацию', request_location=True),
            types.KeyboardButton(text='Ввести вручную')
        )
        builder.row(types.KeyboardButton(text='Отправить геолокацию', request_location=True), types.KeyboardButton(text='Ввести вручную'), types.KeyboardButton(text='В меню'))
        await state.set_state(User.location)
        await messaage.answer('Произошла ошибка, пожалуйста, поделитесь геолокацией снова!',
                             reply_markup=builder.as_markup(resize_keyboard=True))


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

@dp.message(F.text.lower() == 'какой город у меня указан?')
async def whichCity(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        await message.answer(text=f'{data["location"]}')
    except Exception as ex:
        logging.exception(ex)
        await message.answer(text='Я не знаю где вы находитесь!')
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='В меню')
    )
    await message.answer(text=f'{data["location"]}',
                             reply_markup=builder.as_markup(resize_keyboard=True))



async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.message.register(getWather_hendler)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
