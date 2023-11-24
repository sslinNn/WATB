import sqlalchemy
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.model.querys import Request
import emoji
from aiogram import types
from bot.schedule.selected_schedule_parser import get_weekly_schedule_teacher, get_weekly_schedule_group


def get_chocie_day_kb(role: str, class_identifier: str):
    builder = ReplyKeyboardBuilder()
    if role == 'student':
        df = get_weekly_schedule_group(class_identifier)
    else:
        df = get_weekly_schedule_teacher(class_identifier)
    days = [i for i in df['DAY'].unique().tolist()]
    for i in days:
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text='Назад'))
    return builder.as_markup(resize_keyboard=True)