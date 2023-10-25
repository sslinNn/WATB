from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class StartWithUser(StatesGroup):
    yes = State()
    location = State()
    accepting = State()
    tryAgain = State()


class Menu(StatesGroup):
    menu = State()
    menuPicker = State()
    sattings = State()
    weather = State()

class Settings(StatesGroup):
    location = State()
