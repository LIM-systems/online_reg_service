from aiogram import types

from bot.utils.keyboards.common import (admin_main_menu_buttons,
                                        toggle_role_buttons)


def get_admin_main_menu():
    '''Клавиатура главного меню админа'''
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


# рассылка
broadcast_buttons = ('send_broadcast_msg_button',
                     'cancel_broadcast_msg_button')


def get_broadcast_keyboard(only_cancel=False):
    '''Клавиатура рассылки'''
    kb = [[types.InlineKeyboardButton(
        text='Отменить', callback_data=broadcast_buttons[1])]
    ]

    if not only_cancel:
        kb.insert(0, [types.InlineKeyboardButton(
            text='Отправить', callback_data=broadcast_buttons[0])])

    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=kb
    )
    return keyboard
