from aiogram import types

from bot.utils.keyboards.common import (admin_main_menu_buttons,
                                        toggle_role_buttons)


def get_admin_main_menu():
    '''Клавиатура главного меню мастера'''
    kb = [
        [types.KeyboardButton(text=admin_main_menu_buttons[0]),
         types.KeyboardButton(text=admin_main_menu_buttons[1])],
        [types.KeyboardButton(text=toggle_role_buttons[0]),
         types.KeyboardButton(text=toggle_role_buttons[1])],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text_admin = f'''Вам доступны пункты меню:

<b>{admin_main_menu_buttons[0]}</b> – отправка рассылки клиентам, например, о скидках;

<b>{admin_main_menu_buttons[1]}</b> – открыть админку;

<b>{toggle_role_buttons[0]}</b> – переключится на меню клиента;

<b>{toggle_role_buttons[1]}</b> – переключится на меню мастера;

'''
