from aiogram.utils.keyboard import ReplyKeyboardBuilder

def getMenuKB():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Настройки")
    kb.button(text="Погода")
    kb.button(text="Ввести секретный код")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
