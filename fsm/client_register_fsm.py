from aiogram.fsm.state import StatesGroup, State

class RegisterFSM(StatesGroup):
    gender = State()
    age = State()
    height = State()
    weight = State()
    activity_level = State()