import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
from bot.keyboard.emoji_control import remove_emojis
from weather.getWeather import getWeather, parse_api
from weather.graphs import weather_graph
from bot.statements.states import StartWithUser, Menu, Settings, Secrets
from bot.utils.commands import set_commands
from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SettingsKB import getSettingsKB
from bot.keyboard.SecretKB import getNhtkKB
from bot.model.querys import select_location_from_db


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Menu.menu)
async def menu(message: types.Message, state: FSMContext):
    await set_commands(bot)
    if message.text.lower() == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer(f'Меню:', reply_markup=getMenuKB())
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(Menu.menuPicker)
async def menuPicker(message: types.Message, state: FSMContext):
    await set_commands(bot)
    if remove_emojis(message.text.lower()) == 'настройки':
        await state.set_state(Settings.location)
        # location = await state.get_data()
        # await message.answer(f'Вы тут: {location["location"]}', reply_markup=getSettingsKB())
        location = select_location_from_db(id_=message.from_user.id)
        await message.answer(f'Вы тут: {location}', reply_markup=getSettingsKB())
        await state.set_state(Settings.location)
    elif remove_emojis(message.text.lower()) == 'текущая погода':
        await state.set_state(StartWithUser.location)
        data = await state.get_data()
        try:
            await message.answer(text=f'{getWeather(locate=data["location"], weather_api_key=WEATHER_API_KEY)}')
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    elif remove_emojis(message.text.lower()) == 'прогноз погоды на сегодня':
        try:
            await state.set_state(StartWithUser.location)
            data = await state.get_data()
            wait = await bot.send_message(chat_id=message.chat.id, text='Подождите...')
            df, sun, date = parse_api(data['location'], WEATHER_API_KEY)
            photo_content = weather_graph(df, sun, date, data['location'])
            await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
            await bot.send_photo(chat_id=message.chat.id, photo=types.input_file.BufferedInputFile(photo_content, filename="weather.png"))
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    else:
        await message.answer('Такого варианта ответа нет!')


