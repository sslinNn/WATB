import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from weather.getLocaion import getLocationFromCoordinates, getLocationFromCityName
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers
from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from bot.statements.states import StartWithUser, Menu, Settings, Secret


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Secret.secretKey)
async def code(message: types.Message, state: FSMContext):
    await state.set_state(Secret.secretKey)
    keys = {
        'NHTK': ['nhtk', 'нхтк']
    }
    code = message.text.lower()
    if code in keys['NHTK']: #ПОТОМ ПЕРЕДЕЛАЮ!!!
        await state.set_state(Secret.nhtkKey)
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Студент'),
            types.KeyboardButton(text='Преподаватель'),
            types.KeyboardButton(text='В меню')
        )
        builder.adjust(2)
        await message.answer(
            f'Вы ввели код: {code}, вы явно о чем-то знаете!'
            f' Если вы хотите получать расписание, пожалуйста, скажите кто вы?',
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer(
            f'Вы кажется что-то перепутали! Такого кода нет'
        )


@dp.message(Secret.nhtkKey)
async def nhtk(message: types.Message, state: FSMContext):
    if message.text.lower() == 'студент':
        await state.set_state(Secret.getrole)
        df = getScheduleNHTK_groups()
        groups = df['GroupName'].tolist()
        print(len(groups))
        builder = ReplyKeyboardBuilder()
        for i in groups:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(4)
        builder.row(types.KeyboardButton(text='В меню'))
        await message.answer(
            "Выберите группу из списка или введите вручную",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif message.text.lower() == 'преподаватель':
        await state.set_state(Secret.getrole)
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='В меню'))
        await message.answer(
            "Увы, кнопок нет, но вы можете ввести свою фамилию (например: Иванов. И. И.)",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif message.text.lower() == 'в меню':
        await state.set_state(Menu.menuPicker)
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Настройки'),
            types.KeyboardButton(text='Погода'),
            types.KeyboardButton(text='Ввести секретный код')
        )
        builder.adjust(2)
        await message.answer(
            f'Меню:',
            reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(Secret.getrole)
async def get_role(message: types.Message, state: FSMContext):
    df_stud = getScheduleNHTK_groups()
    df_teach = getScheduleNHTK_teachers()
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text='В меню')
    )
    word = message.text
    print(df_stud['GroupName'])
    if word in df_stud['GroupName']:
        await state.set_state(Secret.secretKey)
        await state.update_data({'getrole': ['student', message.text, 'nhtk']})
        await message.answer(
            f'Успешно!', reply_markup=builder.as_markup(resize_keyboard=True)
        )
    elif message.text in df_teach['Name']:
        await state.set_state(Secret.secretKey)
        await state.update_data({'getrole': ['teacher', message.text, 'nhtk']})
        await message.answer(
            f'Успешно!', reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer('Такого варианта ответа нет!')
