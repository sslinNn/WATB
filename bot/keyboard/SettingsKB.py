from aiogram.utils.keyboard import ReplyKeyboardBuilder

def getSettingsKB():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Изменить месторасположения")
    kb.button(text="Меню")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

