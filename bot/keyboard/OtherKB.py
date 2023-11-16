from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji

def yesOrNo():
    kb = ReplyKeyboardBuilder()
    yes_e = emoji.emojize(":check_mark_button:")
    no_e = emoji.emojize(":cross_mark_button:")
    kb.button(text=f"Да{yes_e}")
    kb.button(text=f"Нет{no_e}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def locationKB():
    kb = ReplyKeyboardBuilder()
    map_e = emoji.emojize(":globe_showing_Asia-Australia:")
    mannuly_e = emoji.emojize(":writing_hand:")
    kb.button(text=f"Отправить геолокацию{map_e}", request_location=True)
    kb.button(text=f"Ввести вручную{mannuly_e}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
