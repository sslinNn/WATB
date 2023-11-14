from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji

def getMenuKB():
    gear_emoji = emoji.emojize(":gear:")
    ninja_emoji = emoji.emojize(":ninja:")
    calendar_emoji = emoji.emojize(":calendar:")
    thermometer_emoji = emoji.emojize(":thermometer:")
    kb = ReplyKeyboardBuilder()
    kb.button(text=f"Настройки{gear_emoji}")
    kb.button(text=f"Текущая Погода{thermometer_emoji}")
    kb.button(text=f"Прогноз погоды на сегодня{calendar_emoji}")
    kb.button(text=f"Ввести секретный код{ninja_emoji}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
