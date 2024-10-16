from aiogram import F, types

from bot.loader import router
from bot.utils.keyboards.common import get_role, toggle_role_buttons
from bot.utils.other.common import role_menu


@router.message(F.text.in_(toggle_role_buttons))
async def change_role(msg: types.Message, promo_active: bool):
    '''Обработчик кнопок переключения ролей'''
    promo = promo_active if msg.text == toggle_role_buttons[0] else None
    role = await get_role(msg.from_user.id)
    await role_menu(msg=msg, role=role, promo_active=promo)
