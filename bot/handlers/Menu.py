import logging
import os
import re
import sqlalchemy

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandObject
from dotenv import load_dotenv
from weather.getWeather import getWeather, parse_api
from weather.graphs import weather_graph
from bot.schedule.selected_schedule_parser import (get_weekly_schedule_group,
                                                   get_weekly_schedule_teacher,
                                                   get_daily_schedule)
from bot.statements.states import StartWithUser, Menu, Settings, Secrets, Schedule
from bot.schedule.converting_df_bez_xyini import df_to_pdf, df_to_xlsx, df_to_png
from bot.utils.commands import set_commands
from bot.keyboard.emoji_control import remove_emojis
from bot.keyboard.MenuKB import getMenuKB
from bot.keyboard.SettingsKB import getSettingsKB
from bot.keyboard.SecretKB import getNhtkKB, getScheduleKB
from bot.model.querys import Request


load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Menu.menu)
async def menu(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    await set_commands(bot)
    if message.text.lower() == 'меню':
        await state.set_state(Menu.menuPicker)
        await message.answer(f'Меню:', reply_markup=getMenuKB(message.from_user.id, request))
    else:
        await message.answer('Такого варианта ответа нет!')


@dp.message(Command('code'))
async def secret_code(message: types.Message, command: CommandObject,
                      state: FSMContext, request: sqlalchemy.Connection):
    text = command.args
    if text in ['nhtk', 'нхтк']:
        user_id = message.from_user.id
        await Request(request).insert_code_in_db(user_id)
        await state.set_state(Secrets.nhtk)
        await message.answer(
            f'Вы ввели код: {text}, вы явно о чем-то знаете!'
            f' Если вы хотите получать расписание, пожалуйста, скажите кто вы?',
            reply_markup=getNhtkKB()
        )
    else:
        await message.answer('Такого кода нет!')


@dp.message(Command('available_schedule_pdf'))
async def available_schedule_pdf(message: types.Message, command: CommandObject):
    text = command.args
    if text != None:
        try:
            pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
            pattern_in_message = re.findall(pattern, text)
            if text in pattern_in_message:
                df = get_weekly_schedule_group(text)
                pdf = df_to_pdf(df)
            else:
                df = get_weekly_schedule_teacher(text)
                pdf = df_to_pdf(df)
            await message.answer_document(document=types.input_file.BufferedInputFile(
                    pdf,
                    filename=f"schedule_{text}.pdf"
                ))
        except IndexError as e:
            await message.answer('Убедитесь что вы все указали верно')
            print(e)
    else:
        await message.answer('Введите номер группы или фамилию и инициалы преподователя')


@dp.message(Command('available_schedule_xlsx'))
async def available_schedule_xlsx(message: types.Message, command: CommandObject):
    text = command.args
    if text != None:
        try:
            pattern = r'\d{2}\.\d{2}\.\d{2}[A-Za-zА-Яа-я]?'
            pattern_in_message = re.findall(pattern, text)
            if text in pattern_in_message:
                df = get_weekly_schedule_group(text)
                pdf = df_to_xlsx(df)
            else:
                df = get_weekly_schedule_teacher(text)
                xlsx = df_to_xlsx(df)
            await message.answer_document(document=types.input_file.BufferedInputFile(
                xlsx,
                filename=f"schedule_{text}.xlsx"
            ))
        except IndexError as e:
            await message.answer('Убедитесь что вы все указали верно')
            print(e)
    else:
        await message.answer('Введите номер группы или фамилию и инициалы преподователя')


@dp.message(Command('daily_schedule'))
async def daily_schedule(message: types.Message, command: CommandObject):
    text = command.args
    name = text.split(' ')[0]
    date = text.split(' ')[1]
    if text != None:
        try:
            df = get_daily_schedule(name=name, date=date)
            photo = df_to_png(df)
            await message.answer_photo(photo=types.input_file.BufferedInputFile(
                photo,
                filename=f"schedule_{text}.xlsx"
            ))
        except IndexError as e:
            await message.answer('Убедитесь что вы все указали верно')
            print(e)
    else:
        await message.answer('Введите номер группы или фамилию и инициалы преподователя')


@dp.message(Menu.menuPicker)
async def menuPicker(message: types.Message, state: FSMContext, request: sqlalchemy.Connection):
    await set_commands(bot)
    if remove_emojis(message.text.lower()) == 'настройки':
        await state.set_state(Settings.location)
        location = await state.get_data()
        time = await Request(request).select_notification_time_from_db_by_id(id_=message.from_user.id)
        if time:
            await message.answer(
                f'Вы тут: {location["location"]}\n'
                f'Время уведомлений: {"".join(list(str(time))).split(":")[0]}:{"".join(list(str(time))).split(":")[1]}',
                reply_markup=getSettingsKB()
            )
        else:
            await message.answer(
                f'Вы тут: {location["location"]}',
                reply_markup=getSettingsKB()
            )
        await state.set_state(Settings.settingPicker)
    elif remove_emojis(message.text.lower()) == 'текущая погода':
        await state.set_state(StartWithUser.location)
        try:
            location = await state.get_data()
            await message.answer(text=f'{getWeather({location["location"]}, weather_api_key=WEATHER_API_KEY)}')
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    elif remove_emojis(message.text.lower()) == 'прогноз погоды на сегодня':
        try:
            await state.set_state(StartWithUser.location)
            data = await state.get_data()
            wait = await bot.send_message(
                chat_id=message.chat.id,
                text='Подождите...',
                reply_markup=types.ReplyKeyboardRemove()
            )
            df, sun, date = parse_api(data['location'], WEATHER_API_KEY)
            photo_content = weather_graph(df, sun, date, data['location'])
            await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=types.input_file.BufferedInputFile(
                    photo_content,
                    filename="weather.png"
                ),
                reply_markup=getMenuKB(message.from_user.id, request)
            )
            await state.set_state(Menu.menuPicker)
        except Exception as ex:
            logging.exception(ex)
            await message.answer(text='Я не знаю где вы находитесь!')
    elif remove_emojis(message.text.lower()) == 'команды':
        user_id = message.from_user.id
        text = (f'/start - Начало\n'
                f'/code - Ввести секретный код')
        secret_part = (f' (для того чтобы что-то изменить в настройках расписания, вы можете заново ввести код)\n'
                f'/available_schedule_pdf - Получить доступное расписание в .pdf '
                f'(после команды нужно ввести номер группы и если вы преподователь - фамилию и инициалы)\n'
                f'/available_schedule_xlsx - Получить доступное расписание в .xlsx '
                f'(после команды нужно ввести номер группы и если вы преподователь - фамилию и инициалы)\n'
                f'/daily_schedule - Расписание на определенный день\n'
                f'(после команды введите сначала группу или фамилию и инициалы преподавателя и дату\n'
                f'Пример: /daily_schedule 09.07.11 23.11.2023)')
        code_nhtk = await Request(request).select_code_in_db(user_id)
        if code_nhtk:
            text += secret_part
        await message.answer(text)
    elif remove_emojis(message.text.lower()) == 'расписание':
        user_id = message.from_user.id
        await state.set_state(Schedule.schedule)
        text = 'Расписание:'
        await message.answer(text, reply_markup=getScheduleKB())
    else:
        await message.answer('Такого варианта ответа нет!')
