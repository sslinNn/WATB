import datetime
import asyncio
import logging
import os
import sys
import pandas as pd
from tabulate import tabulate
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandObject, Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv
from schedule.converting_df import df_to_png
from statements.states import StartWithUser, Menu, Settings, Secret
from aiogram.types import InputMediaPhoto, FSInputFile
from handlers.StartWithUser import message_handler, yes, location, accepting
from handlers.Menu import menu, menuPicker
from handlers.Settings import changeLocate
from handlers.SecretCode import code, nhtk, get_role

from schedule.selected_schedule_parser import get_daily_schedule, get_weekly_schedule_teacher, get_weekly_schedule_group
from schedule.all_schedule_parser import getScheduleNHTK_groups, getScheduleNHTK_teachers



load_dotenv()
TOKEN = os.getenv('TGBOT_API_KEY')
TOKENYA = os.getenv('YANDEX_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
bot = Bot(token=TOKEN)
dp = Dispatcher()



"""
ВРОДЕ ВСЁ ПОФИКСИЛ. ПОКРАЙНЕЙ МЕРЕ НАДЕЮСЬ НА ЭТО!

КАРОЧЕ ТО, ЧТО ЗАКОММЕНЧЕНО НАДО ПОДСТРОИТЬ К РУЧНОМУ ВВОДУ МЕСТОПОЛОЖЕНИЯ (StartWithUser.py def's: accepting, location)
А ТО, ЧТО НЕ ЗАКОММЕНЧЕНО НАДО РАСПИХАТЬ ПО ХЭНДЛЕРАМ
Я МЕНЮШКУ ТВОЮ ПЕРЕДЕЛАЛ КНОПКА ВВЕСТИ КОД ЕСТЬ, НО КОГДА НА НЕЁ ЖМЕШЬ ПЕРЕКИДЫВАЕТ НА ОБЫЧНЫЙ ХЭНДЛЕР И ВСЁ ЛОМАЕТСЯ,
ЗАВТРА ЗАЙМУСЬ ЭТИМ ВОПРОСОМ

ВООБЩЕ, БЫЛО БЫ ЗДОРОВО, ЕСЛИ БЫ ТЫ ПОПЫТАЛСЯ ХОТЯБЫ РАЗОБРАТСЯ ЧЕ Я НАМУДРИЛ СО СТЕЙТАМИ И ПЕРЕХОДОМ ПО ХЕНДЛЕРАМ
ДУМАЮ, ТАК ЯСНЕЕ СТАНЕТ КАК ПРОДОЛЖАТЬ ДЕЛАТЬ ВООБЩЕ
"""





@dp.message(Command(commands=['tomorrow_schedule']))
@dp.message(F.text.lower() == 'расписание на завтра')
async def tomorrow_schedule(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_new = '.'.join(str(tomorrow).split('-')[::-1])
    df = get_daily_schedule('09.07.11', tomorrow_new)

    df_str = df.to_string(index=False)
    path = df_to_png(df)
    photo = FSInputFile('output/output.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)


@dp.message(Command(commands=['weekly_schedule']))
@dp.message(F.text.lower() == 'расписание на неделю')
async def tomorrow_schedule(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text='В меню'))
    df = get_weekly_schedule_group('09.07.11')
    df_str = df.to_string(index=False)
    path = df_to_png(df)
    photo = FSInputFile('output/output.png')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)




# @dp.message(F.text.lower() == 'ввести вручную')
# async def whereIamManually(message: types.Message):
#     await message.answer(text='Хорошо, введите ваш город после /city')
# @dp.message(Command(commands=['city']))
# async def manuallyCity(message: types.Message, state: FSMContext, command: CommandObject):
#     if command.args:
#         builder = ReplyKeyboardBuilder()
#         builder.row(
#             types.KeyboardButton(text='Какой город у меня указан?'), types.KeyboardButton(text='В меню')
#         )
#         city, country, fixed = getLocationFromCityName(TOKEN=TOKENYA, NAME=str(command.args))
#         if fixed:
#             await message.answer(f"Установлен город: {city}, страна: {country}",
#                              reply_markup=builder.as_markup(resize_keyboard=True))
#             await state.update_data({'location': city})
#         else:
#             await message.answer(f"Вы допустили ошибку, будет выбран город: {city}, страна: {country}",
#                              reply_markup=builder.as_markup(resize_keyboard=True))
#             await state.update_data({'location': city})
#     else:
#         await message.answer("Пожалуйста, введите ваш город после /city")





async def main():
    bott = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp.message.register(message_handler, CommandStart())
    dp.message.register(yes, StartWithUser.yes)
    dp.message.register(location, StartWithUser.location)
    dp.message.register(accepting, StartWithUser.accepting)
    dp.message.register(menu, Menu.menu)
    dp.message.register(menuPicker, Menu.menuPicker)
    dp.message.register(changeLocate, Settings.location)
    # dp.message.register(code, Secret.secretKey)
    # dp.message.register(nhtk, Secret.nhtkKey)
    # dp.message.register(get_role, Secret.getrole)
    await dp.start_polling(bott)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
