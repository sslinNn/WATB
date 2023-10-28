import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from weather.getLocaion import getLocationFromCoordinates

from bot.statements.states import StartWithUser, Menu, Settings

from bot.keyboard.OtherKB import locationKB, yesOrNo
from bot.keyboard.MenuKB import getMenuKB

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
            await message.answer(
                text=f'Отправь локацию, или введи вручную',
                reply_markup=locationKB()
            )
        elif message.text.lower() == 'меню':
            await state.set_state(Menu.menuPicker)
            await message.answer(
                f'Меню:',
                reply_markup=getMenuKB()
            )
        elif message.text.lower() == 'ввести вручную':
            await state.set_state(StartWithUser.accepting)
            await message.answer(text=f'Введите название вашего месторасположения')
        else:
            await state.set_state(StartWithUser.accepting)
            await state.update_data({'location': message.text.title()})
            await message.answer(
                f'Вы находитесь в: {message.text.title()}?',
                reply_markup=yesOrNo()
            )
    except AttributeError:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=yesOrNo())
