from aiogram.utils.keyboard import ReplyKeyboardBuilder

def getNhtkKB():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Студент")
    kb.button(text="Преподаватель")
    kb.button(text="Меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def getScheduleKB():
    kb = ReplyKeyboardBuilder()
    kb.button(text="Расписание на завтра")
    kb.button(text="Расписание на неделю")
    kb.button(text="Меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
