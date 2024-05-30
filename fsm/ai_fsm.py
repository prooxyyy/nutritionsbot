from aiogram.fsm.state import StatesGroup, State

class AIGenerateReceiptFSM(StatesGroup):
    text = State()
    photo = State()