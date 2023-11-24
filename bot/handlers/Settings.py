import os

import sqlalchemy
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from bot.keyboard.emoji_control import remove_emojis
from weather.getLocaion import getLocationFromCoordinates

from bot.statements.states import StartWithUser, Menu, Settings

from bot.keyboard.OtherKB import locationKB, yesOrNo
from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SettingsKB import timeKB, getSettingsKB

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Settings.settingPicker)
async def changeLocate(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    try:
        if remove_emojis(message.text.lower()) == 'изменить месторасположения':
            await state.set_state(StartWithUser.accepting)
            await message.answer(
                text=f'Отправь локацию, или введи вручную',
                reply_markup=locationKB()
            )
        elif remove_emojis(message.text.lower()) == 'установить время уведомлений':
            await state.set_state(Settings.notification_time)
            await message.answer(text=f'Выберите время, в которое хотите получать уведомления', reply_markup=timeKB())


        elif remove_emojis(message.text.lower()) == 'меню':
            await state.set_state(Menu.menuPicker)
            await message.answer(
                f'Меню:',
                reply_markup=getMenuKB(message.from_user.id, request)
            )

        else:
            await message.answer(f'Я не знаю что ты хочешь от меня, выбери из кнопок)')
    except AttributeError:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(f'Вы находитесь в: {userLocation}?', reply_markup=yesOrNo())

@dp.message(Settings.notification_time)
async def set_notification_time(message: types.Message, state: FSMContext):
    await state.set_state(Settings.notification_time)
    await state.update_data({'notification_time': message.text})
    time = await state.get_data()
    await message.answer(f'Вы будете получать уведемления в {time["notification_time"]}', reply_markup=getSettingsKB())
    await state.set_state(Settings.settingPicker)
