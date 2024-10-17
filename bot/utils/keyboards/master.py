from aiogram import types
from bot.utils.keyboards.common import (master_main_menu_buttons, my_profile_button,
                                        toggle_role_buttons)


def get_master_main_menu(admin_button=None):
    '''Клавиатура главного меню мастера'''
    kb = [
        [types.KeyboardButton(text=my_profile_button),
         types.KeyboardButton(text=master_main_menu_buttons[0])],
        [types.KeyboardButton(text=master_main_menu_buttons[1]),
         types.KeyboardButton(text=toggle_role_buttons[0])],
    ]

    if admin_button:  # кнопки переключение на админа
        kb.append([types.KeyboardButton(text=admin_button)])

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text_master = f'''Вам доступны пункты меню:

<b>{my_profile_button}</b> – здесь можно изменить привязанный телефон и ФИО, посмотреть свои записи и историю записей;

<b>{master_main_menu_buttons[0]}</b> – посмотреть свой график и записи клиентов к Вам;

<b>{master_main_menu_buttons[1]}</b> – Оценки клиентов за определённый период и Ваш общий бал;

<b>{toggle_role_buttons[0]}</b> – переключится на меню клиента;

'''
