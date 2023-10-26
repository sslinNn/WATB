from aiogram.fsm.state import StatesGroup, State

class User(StatesGroup):
    location = State()