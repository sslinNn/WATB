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


class Settings(StatesGroup):
    location = State()


class Secret(StatesGroup):
    secretKey = State()
    nhtkKey = State()
    role = State()
    getrole = State()