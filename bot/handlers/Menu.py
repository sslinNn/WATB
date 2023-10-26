import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from weather.getWeather import getWeather

from bot.statements.states import StartWithUser, Menu, Settings



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
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Настройки'),
            types.KeyboardButton(text='Погода'),
            types.KeyboardButton(text='Ввести секретный код')
        )
        builder.adjust(2)
        await message.answer(
            f'Меню:',
            reply_markup=builder.as_markup(resize_keyboard=True)
        )
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(Menu.menuPicker)
async def menuPicker(message: types.Message, state: FSMContext):
    if message.text.lower() == 'настройки':
        await state.set_state(Settings.location)
        builder = ReplyKeyboardBuilder()
        builder.row(
            types.KeyboardButton(text='Изменить месторасположения'),
            types.KeyboardButton(text='Меню')
        )
        builder.adjust(1)
        data = await state.get_data()
        await message.answer(f'Вы тут: {data["location"]}', reply_markup=builder.as_markup(resize_keyboard=True))
        await state.set_state(Settings.location)

    elif message.text.lower() == 'погода':
        await state.set_state(StartWithUser.location)
        data = await state.get_data()
        try:
            await message.answer(text=f'{getWeather(locate=data["location"], weather_api_key=WEATHER_API_KEY)}')
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    else:
        await message.answer('Такого варианта ответа нет!')
