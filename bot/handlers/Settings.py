import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather.getLocaion import getLocationFromCoordinates


from bot.statements.states import StartWithUser, Menu, Settings

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Settings.location)
async def changeLocate(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() == 'изменить месторасположения':
            await state.set_state(StartWithUser.accepting)
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text='Отправить геолокацию', request_location=True),
                types.KeyboardButton(text='Ввести вручную')
            )
            await message.answer(
                text=f'Отправь локацию, или введи вручную',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
        elif message.text.lower() == 'главное меню':
            await state.set_state(Menu.menuPicker)
            builder = ReplyKeyboardBuilder()
            builder.row(
                types.KeyboardButton(text='Настройки'),
                types.KeyboardButton(text='Погода')
            )
            await message.answer(
                f'Меню:',
                reply_markup=builder.as_markup(resize_keyboard=True))
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
            await message.answer(f'Вы находитесь в: {message.text.title()}?',
                                 reply_markup=builder.as_markup(resize_keyboard=True))
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
        await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=builder.as_markup(resize_keyboard=True))
