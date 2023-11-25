import sqlalchemy
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji
from bot.model.querys import Request


def getMenuKB(user_id, request: sqlalchemy.Connection):
    class_identifier = Request(request).select_code_in_db(user_id)
    gear_emoji = emoji.emojize(":gear:")
    calendar_emoji = emoji.emojize(":calendar:")
    thermometer_emoji = emoji.emojize(":thermometer:")
    clipboard_emoji = emoji.emojize(":clipboard:")
    schedule_e = emoji.emojize(":spiral_notepad:")
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Текущая Погода{thermometer_emoji}")
    kb.button(text=f"Прогноз погоды на сегодня{calendar_emoji}")
    if class_identifier:
        kb.button(text=f"Расписание{schedule_e}")
    kb.button(text=f"Настройки{gear_emoji}")
    kb.button(text=f"Команды{clipboard_emoji}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
