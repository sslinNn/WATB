import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv

from bot.model.querys import insert_id_and_location_in_db

from weather.getLocaion import getLocationFromCoordinates, getLocationFromCityName

from bot.statements.states import StartWithUser, Menu

from bot.keyboard.OtherKB import yesOrNo, locationKB


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
        await message.answer('Тогда поделись со мной своей геолокацией, пожалуйста!',
                             reply_markup=locationKB())
    else:
        await message.answer('Я не понимаю, о чем ты')

@dp.message(StartWithUser.location)
async def location(message: types.Message, state: FSMContext):
    if message.location is not None:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=yesOrNo())
    elif message.text.lower() == 'ввести вручную':
        await state.set_state(StartWithUser.accepting)
        await message.answer(f'Введите название вашего месторасположения', reply_markup=types.ReplyKeyboardRemove())
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
            user_id = message.from_user.id
            location_ = await state.get_data()
            insert_id_and_location_in_db(user_id, location_.get('location'))
        elif message.text.lower() == 'нет':
            await state.set_state(StartWithUser.accepting)
            await message.answer(
                text=f'Попробуйте снова, или введите название вашего месторасположения вручную',
                reply_markup=locationKB()
            )
        elif message.text.lower() == 'ввести вручную':
            await state.set_state(StartWithUser.accepting)
            await message.answer(text=f'Введите название вашего месторасположения', reply_markup=types.ReplyKeyboardRemove())
        else:
            await state.set_state(StartWithUser.accepting)
            city, country, fixed = getLocationFromCityName(TOKENYA, message.text.title())
            if fixed:
                await state.update_data({'location': city})
                await message.answer(
                    f'Кажется вы неправильно ввели город: {message.text.title()}, '
                    f'вы находитесь в: {city}, страна {country}?',
                    reply_markup=yesOrNo()
                )
            else:
                await state.update_data({'location': city})
                await message.answer(
                    f'Вы находитесь в: {city}, страна {country}?',
                    reply_markup=yesOrNo()
                )

    except AttributeError:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(
            f'Вы находитесь в: {userLocation}?', reply_markup=yesOrNo()
        )
