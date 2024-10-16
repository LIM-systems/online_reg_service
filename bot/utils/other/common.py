from bot.utils.keyboards.client import get_client_main_menu, promo_menu_text, start_menu_text


async def role_menu(**kwargs):
    '''Отображение меню для каждой роли'''
    role = kwargs.get('role', 'client')
    msg = kwargs.get('msg')
    promo_active = kwargs.get('promo_active')

    if role == 'client':
        text = start_menu_text if not promo_active else start_menu_text + promo_menu_text
        await msg.answer(text, reply_markup=get_client_main_menu(promo_active))
    if role == 'master':
        await msg.answer('меню мастера')
    if role == 'admin':
        await msg.answer('меню админа')
