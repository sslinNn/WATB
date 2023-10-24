from aiogram.fsm.state import State, StatesGroup

class StartWithUser(StatesGroup):
    yes = State()
    location = State()
    accepting = State()