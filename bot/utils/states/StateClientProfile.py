from aiogram.fsm.state import State, StatesGroup


class ClientProfile(StatesGroup):
    name = State()
    phone = State()
    email = State()
    verify_code = State()


class ListOfLoayalityProgramm(StatesGroup):
    name = State()
    loaylity_promos_list = State()
