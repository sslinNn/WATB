import asyncio
import logging
import os
import sys
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from weather.getLocaion import getLocationFromCoordinates
from User import User

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
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


#for push
@dp.message(F.text.lower() == 'да')
async def whereIam(messaage: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await messaage.answer(text=f'{data["location"]}')
    except KeyError:
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Отправить геолокацию', request_location=True))
        await state.set_state(User.location)
        await messaage.answer('Произошла ошибка, пожалуйста, поделитесь геолокацией снова!',
                             reply_markup=builder.as_markup(resize_keyboard=True))



@dp.message(F.text.lower() == 'да')
async def whereIam(messaage: types.Message, state: FSMContext):
    data = await state.get_data()
    await messaage.answer(text=f'{data["location"]}')



async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
