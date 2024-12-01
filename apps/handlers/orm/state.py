from aiogram.fsm.state import StatesGroup, State


class FindName(StatesGroup):
    name = State()
    msg_id = State()
