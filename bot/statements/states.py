from aiogram.fsm.state import State, StatesGroup


class StartWithUser(StatesGroup):
    yes = State()
    location = State()
    accepting = State()


class Menu(StatesGroup):
    menu = State()
    menuPicker = State()

    sattings = State()
    weather = State()
    secretKey = State()

class Secrets(StatesGroup):
    code = State()
    nhtk = State()
    nhtkGroup = State()
    schedulePicker = State()

class Settings(StatesGroup):
    location = State()
