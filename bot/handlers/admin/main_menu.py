from aiogram.fsm.context import FSMContext
from aiogram import F, types

from bot.loader import router
from bot.utils.keyboards.common import admin_main_menu_buttons
from bot.utils.keyboards.admin import get_broadcast_keyboard
from bot.utils.states.StateAdminMenu import AdminMenu


### Рассылка ###
@router.message(F.text == admin_main_menu_buttons[0])
async def master_ratings(msg: types.Message, state: FSMContext):
    '''Рассылка сообщения всем клиентам'''
    await msg.answer('Пришлите сообщение', reply_markup=get_broadcast_keyboard(only_cancel=True))
    await state.set_state(AdminMenu.message)
