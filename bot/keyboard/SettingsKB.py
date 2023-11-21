from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
import emoji


def getSettingsKB():
    kb = ReplyKeyboardBuilder()
    compas_e = emoji.emojize(":compass:")
    menu_e = emoji.emojize("📋")
    time_e = emoji.emojize("⏰")
    kb.button(text=f"Изменить месторасположения{compas_e}")
    kb.button(text=f"Установить время уведомлений{time_e}")
    kb.button(text=f"Меню{menu_e}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def timeKB():
    time_list = [
        "07:00", "08:00", "09:00",
        "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00",
        "16:00", "17:00", "18:00",
        "19:00", "20:00", "21:00",
        "22:00", "23:00", "00:00",
        "01:00", "02:00", "03:00",
        "04:00", "05:00", "06:00"
    ]
    builder = ReplyKeyboardBuilder()
    for i in time_list:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text='Меню'))  # Отдельная строка для "В меню"
    return builder.as_markup(resize_keyboard=True)

