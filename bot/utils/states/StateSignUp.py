from aiogram.fsm.state import State, StatesGroup


class SignUp(StatesGroup):
    first_buttons = State()
    on_or_up = State()
    name = State()
    phone = State()
    email = State()
    verify_code = State()
