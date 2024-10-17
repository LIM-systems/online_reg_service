from bot.utils.keyboards.client import get_client_main_menu, promo_menu_text, start_menu_text
from bot.utils.keyboards.common import toggle_role_buttons
from bot.utils.keyboards.master import get_master_main_menu, start_menu_text_master
from bot.utils.keyboards.admin import get_admin_main_menu, start_menu_text_admin


async def role_menu(**kwargs):
    '''Отображение меню для каждой роли'''

    # данные из аргументов
    roles = kwargs.get('roles')
    active_role = roles.get('active')
    master, admin = roles.get('exists').get(
        'master'), roles.get('exists').get('admin')
    msg = kwargs.get('msg')
    promo_active = kwargs.get('promo_active')

    if active_role == 'client':
        # если активная роль клиента
        text = start_menu_text if not promo_active else start_menu_text + promo_menu_text

        # доступные роли для отображения кнопок переключения
        if master and admin:
            role_buttons = toggle_role_buttons[1:]
        elif master:
            role_buttons = [toggle_role_buttons[1]]
        else:
            role_buttons = [toggle_role_buttons[2]]

        await msg.answer(text, reply_markup=get_client_main_menu(promo_active, role_buttons=role_buttons))

    if active_role == 'master':
        # если активная роль мастера

        # если доступна роль админа
        if admin:
            kb = get_master_main_menu(admin_button=toggle_role_buttons[2])
        else:
            kb = get_master_main_menu()
        await msg.answer(start_menu_text_master, reply_markup=kb)

    if active_role == 'admin':
        # если активна роль мастера
        await msg.answer(start_menu_text_admin, reply_markup=get_admin_main_menu())
