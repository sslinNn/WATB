import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from weather.getLocaion import getLocationFromCoordinates

from bot.statements.states import StartWithUser, Menu


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def message_handler(message: types.Message, state: FSMContext):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='Да!'))
    await state.set_state(StartWithUser.yes)
    await message.answer(f'Привет! Хочешь узнать погоду?', reply_markup=builder.as_markup(resize_keyboard=True))



@dp.message(StartWithUser.yes)
async def yes(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да!':
        await state.set_state(StartWithUser.location)
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Отправить геолокацию', request_location=True),
            types.KeyboardButton(text='Ввести вручную')
        )
        await message.answer('Тогда поделись со мной своей геолокацией, пожалуйста!',
                             reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await message.answer('Я не понимаю, о чем ты')

@dp.message(StartWithUser.location)
async def location(message: types.Message, state: FSMContext):
    if message.location is not None:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Да'),
            types.KeyboardButton(text='Нет')
        )
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=builder.as_markup(resize_keyboard=True))
    elif message.text.lower() == 'ввести вручную':
        await state.set_state(StartWithUser.accepting)
        await message.answer(f'Введите название вашего месторасположения')
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(StartWithUser.accepting)
async def accepting(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() == 'да':
            await state.set_state(Menu.menu)
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text='Меню')
            )
            await message.answer(
                text=f'Настройка бота готова, Добро Пожаловать!',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
        elif message.text.lower() == 'нет':
            await state.set_state(StartWithUser.accepting)
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text='Отправить геолокацию', request_location=True),
                types.KeyboardButton(text='Ввести вручную')
            )
            await message.answer(
                text=f'Попробуйте снова, или введите название вашего месторасположения вручную',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
        elif message.text.lower() == 'ввести вручную':
            await state.set_state(StartWithUser.accepting)
            await message.answer(text=f'Введите название вашего месторасположения')
        else:
            await state.set_state(StartWithUser.accepting)
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text='Да'),
                types.KeyboardButton(text='Нет')
            )
            await state.update_data({'location': message.text.title()})
            await message.answer(
                f'Вы находитесь в: {message.text.title()}?', reply_markup=builder.as_markup(resize_keyboard=True)
            )
    except AttributeError:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Да'),
            types.KeyboardButton(text='Нет')
        )
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(
            f'Вы находитесь в: {userLocation}?', reply_markup=builder.as_markup(resize_keyboard=True)
        )
