from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji


def getSettingsKB():
    kb = ReplyKeyboardBuilder()
    compas_e = emoji.emojize(":compass:")
    menu_e = emoji.emojize("📋")
    kb.button(text=f"Меню{menu_e}")
    kb.button(text=f"Изменить месторасположения{compas_e}")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
