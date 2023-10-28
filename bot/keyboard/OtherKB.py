from aiogram.utils.keyboard import ReplyKeyboardBuilder

def yesOrNo():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да")
    kb.button(text="Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def locationKB():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить геолокацию", request_location=True)
    kb.button(text="Ввести вручную")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
