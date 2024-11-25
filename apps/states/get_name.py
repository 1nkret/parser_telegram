from aiogram.fsm.state import State, StatesGroup


class GetName(StatesGroup):
    name = State()
    msg_id = State()
    message_id = State()
    input_msg_id = State()
