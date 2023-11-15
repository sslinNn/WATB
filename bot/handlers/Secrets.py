import datetime
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from bot.keyboard.emoji_control import remove_emojis
from bot.statements.states import Menu, Secrets

from bot.schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_group
from bot.schedule.all_schedule_parser import getScheduleNHTK_groups

from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SecretKB import getNhtkKB, getScheduleKB

load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Secrets.code)
async def code(message: types.Message, state: FSMContext):
    if message.text.lower() == 'nhtk' or message.text.lower() == 'нхтк':
        await state.set_state(Secrets.nhtk)
        await message.answer(
            f'Вы ввели код: {message.text}, вы явно о чем-то знаете!'
            f' Если вы хотите получать расписание, пожалуйста, скажите кто вы?',
            reply_markup=getNhtkKB()
        )
    else:
        await message.answer('Такого кода нет!')

async def nhtk(message: types.Message, state: FSMContext):
    if remove_emojis(message.text.lower()) == 'студент':
        # await state.clear()
        await state.set_state(Secrets.nhtkGroup)
        df = getScheduleNHTK_groups()
        groups = df['GroupName'].tolist()
        print(len(groups))
        builder = ReplyKeyboardBuilder()
        for i in groups:
            builder.add(types.KeyboardButton(text=str(i)))
        builder.adjust(4)
        builder.row(types.KeyboardButton(text='Меню'))  # Отдельная строка для "В меню"
        await message.answer(
            "Выберите группу из списка или введите вручную",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif remove_emojis(message.text.lower()) == 'преподаватель':
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))  # Отдельная строка для "В меню"
        await message.answer(
            "Увы, кнопок нет, но вы можете ввести свою фамилию (например: Иванов. И. И.)",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB())
    else:
        await message.answer('Такого варианта ответа нет!')


async def nhtkGroup(message: types.Message, state: FSMContext):
    pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
    patternInMessage = re.findall(pattern, message.text)
    if message.text in patternInMessage:
        await state.set_state(Secrets.schedulePicker)
        await state.update_data({'group': message.text})
        group = await state.get_data()
        await message.answer(
            f'Ваша группа: {group["group"]} '
            f'Что хотите узнать?',
            reply_markup=getScheduleKB()
        )
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB())
    else:
        await message.answer('ЧТо?')



async def schedulePicker(message: types.Message, state: FSMContext):
    if remove_emojis(message.text.lower()) == 'расписание на завтра':
        await state.set_state(Secrets.schedulePicker)
        group = await state.get_data()
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow_new = '.'.join(str(tomorrow).split('-')[::-1])
        df = get_daily_schedule(group["group"], tomorrow_new)
        df_str = df.to_string(index=False)
        # print(df_str)
        photo = FSInputFile('schedule/output/1.png')
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    elif remove_emojis(message.text.lower()) == 'расписание на неделю':
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        await state.set_state(Secrets.schedulePicker)
        group = await state.get_data()
        df = get_weekly_schedule_group(group["group"])
        df_str = df.to_string(index=False)
        # print(df_str)
        photo = FSInputFile('schedule/output/1.png')
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB())
    else:
        await message.answer('Не знаю такх ответов!')
