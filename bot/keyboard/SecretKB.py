from aiogram.utils.keyboard import ReplyKeyboardBuilder
import emoji


def getNhtkKB():
    kb = ReplyKeyboardBuilder()
    student_e = emoji.emojize(":student:")
    teacher_e = emoji.emojize(":teacher:")
    menu_e = emoji.emojize("📋")
    kb.button(text=f"Студент{student_e}")
    kb.button(text=f"Преподаватель{teacher_e}")
    kb.button(text=f"Меню{menu_e}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def getScheduleKB():
    kb = ReplyKeyboardBuilder()
    menu_e = emoji.emojize("📋")
    schedule_e = emoji.emojize(":spiral_notepad:")
    kb.button(text=f"Расписание на завтра{schedule_e}")
    kb.button(text=f"Расписание на сегодня{schedule_e}")
    kb.button(text=f"Расписание на ...{schedule_e}")
    kb.button(text=f"Всё доступное расписание{schedule_e}")
    kb.button(text=f"Меню{menu_e}")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
