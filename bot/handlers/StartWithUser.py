import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from dotenv import load_dotenv
from bot.model.querys import insert_id_and_location_in_db
import io
from weather.getLocaion import getLocationFromCoordinates, getLocationFromCityName, get_location_photo, get_location_from_city_name

from bot.statements.states import StartWithUser, Menu

from bot.keyboard.OtherKB import yesOrNo, locationKB


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
TOKENYAMAP = os.getenv('YANDEX_API_KEY_MAP')
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
            city = message.text.title()
            builder = ReplyKeyboardBuilder()
            locations, cords = get_location_from_city_name(TOKENYA, city)
            if len(locations) > 1:
                await state.set_state(StartWithUser.numbers)
                await state.update_data({'location': city})
                output = ''
                for i in range(len(locations)):
                    output += f'{i+1}. ' + locations[i] + '\n'
                    builder.add(types.KeyboardButton(text=str(i+1)))
                builder.row(types.KeyboardButton(text='Отправить геопозицию'))
                builder.adjust(2)
                output += '\nЕсли в списке нет вашего местоположения, пожалуйста, отправьте геопозицию'
                await message.answer(text=f'Найдено несколько совпадений, выберете номер:\n'
                                          f'{output}',
                                     reply_markup=builder.as_markup(resize_keyboard=True))
            else:
                await state.update_data({'location': city})
                await message.answer(
                    f'Вы находитесь в: {locations[0]}?',
                    reply_markup=yesOrNo()
                )
                photo_content = get_location_photo(TOKENYAMAP, lat=cords[0][0], long=cords[0][1])
                await bot.send_photo(chat_id=message.chat.id, photo=types.input_file.BufferedInputFile(photo_content,
                                                                                                       filename="map.png"))


    except AttributeError:
        await state.set_state(StartWithUser.accepting)
        lon = message.location.longitude
        lat = message.location.latitude
        userLocation = getLocationFromCoordinates(TOKEN=TOKENYA, longitude=lon, latitude=lat)
        await state.update_data({'location': userLocation})
        await message.answer(
            f'Вы находитесь в: {userLocation}?', reply_markup=yesOrNo()
        )


@dp.message(StartWithUser.numbers)
async def location_by_number(message: types.Message, state: FSMContext):
    if 0 < int(message.text) < 11:
        await state.set_state(StartWithUser.location)
        data = await state.get_data()
        city = data['location']
        await state.set_state(StartWithUser.accepting)
        locations, cords = get_location_from_city_name(TOKENYA, city)
        await state.update_data({'location': locations[int(message.text)-1]})
        await message.answer(
            f'Вы находитесь в: {locations[int(message.text)-1]}?',
            reply_markup=yesOrNo()
        )
        photo_content = get_location_photo(TOKENYAMAP, lat=cords[int(message.text)-1][0],
                                           long=cords[int(message.text)-1][1])
        await bot.send_photo(chat_id=message.chat.id, photo=types.input_file.BufferedInputFile(photo_content,
                                                                                               filename="map.png"))
