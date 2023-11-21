import datetime
import os
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from bot.statements.states import Menu, Secrets

from bot.schedule.converting_df_bez_xyini import df_to_png
from bot.schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_group, get_weekly_schedule_teacher
from bot.schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers

from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SecretKB import getNhtkKB, getScheduleKB
from bot.keyboard.emoji_control import remove_emojis


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


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
        builder.row(types.KeyboardButton(text='Меню'))
        await message.answer(
            "Выберите группу из списка или введите вручную",
            reply_markup=builder.as_markup(resize_keyboard=True),
        )
    elif remove_emojis(message.text.lower()) == 'преподаватель':
        await state.set_state(Secrets.nhtkTeacher)
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
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



async def nhtkTeacher(message: types.Message, state: FSMContext):
    teacher = message.text
    df = getScheduleNHTK_teachers()
    for i in df['Name']:
        if teacher == i:
            await state.set_state(Secrets.schedulePicker)
            await state.update_data({'group': teacher})
            group = await state.get_data()
            await message.answer(
                f'{group["group"]}, что хотите узнать?',
                reply_markup=getScheduleKB()
            )
    else:
        await message.answer('Попробуйте снова')
    if remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB())
        
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
        photo = df_to_png(df)
        await bot.send_photo(chat_id=message.chat.id,
                             photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
    elif remove_emojis(message.text.lower()) == 'расписание на неделю':
        builder = ReplyKeyboardBuilder()
        builder.row(types.KeyboardButton(text='Меню'))
        await state.set_state(Secrets.schedulePicker)
        group = await state.get_data()
        pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
        pattern_in_message = re.findall(pattern, group["group"])
        try:
            if group["group"] in pattern_in_message:
                df = get_weekly_schedule_group(group["group"])
                photo = df_to_png(df)
            else:
                df = get_weekly_schedule_teacher(group["group"])
                photo = df_to_png(df)
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=types.input_file.BufferedInputFile(photo, filename="schedule.png"))
        except AttributeError as e:
            await message.answer(text='Кажется такой даты нет!')
    elif remove_emojis(message.text.lower()) == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer('Меню: ', reply_markup=getMenuKB())
    else:
        await message.answer('Не знаю такх ответов!')
