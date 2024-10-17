from aiogram import F, types

from bot.loader import router
from bot.utils.keyboards.common import get_roles, toggle_role_buttons
from bot.utils.other.common import role_menu
from bot.db_reqs import common as db_common


@router.message(F.text.in_(toggle_role_buttons))
async def change_role(msg: types.Message, promo_active: bool):
    '''Обработчик кнопок переключения ролей'''
    # переключение роли
    selected_role = 'client'
    if msg.text == toggle_role_buttons[1]:
        selected_role = 'master'
    elif msg.text == toggle_role_buttons[2]:
        selected_role = 'admin'

    await db_common.toggle_role(msg.from_user.id, selected_role)

    promo = promo_active if msg.text == toggle_role_buttons[0] else None
    roles = await get_roles(msg.from_user.id)
    await role_menu(msg=msg, roles=roles, promo_active=promo)
