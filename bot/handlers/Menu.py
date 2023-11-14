import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from weather.getWeather import getWeather, parse_api
from weather.graphs import weather_graph
from bot.statements.states import StartWithUser, Menu, Settings, Secrets

from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SettingsKB import getSettingsKB


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Menu.menu)
async def menu(message: types.Message, state: FSMContext):
    if message.text.lower() == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer(f'Меню:', reply_markup=getMenuKB())
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(Menu.menuPicker)
async def menuPicker(message: types.Message, state: FSMContext):
    if message.text.lower() == 'настройки':
        await state.set_state(Settings.location)
        data = await state.get_data()
        await message.answer(f'Вы тут: {data["location"]}', reply_markup=getSettingsKB())
        await state.set_state(Settings.location)

    elif message.text.lower() == 'текущая погода':
        await state.set_state(StartWithUser.location)
        data = await state.get_data()
        try:
            await message.answer(text=f'{getWeather(locate=data["location"], weather_api_key=WEATHER_API_KEY)}')
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    elif message.text.lower() == 'прогноз погоды на сегодня':
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
    elif message.text.lower() == 'ввести секретный код':
        await state.set_state(Secrets.code)
        await message.answer('Введите секретный код!', reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer('Такого варианта ответа нет!')
