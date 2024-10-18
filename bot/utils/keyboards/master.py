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
        keyboard=kb,
    )

    return keyboard


start_menu_text_master = f'''Вам доступны пункты меню:

<b>{my_profile_button}</b> – здесь можно изменить привязанный телефон и ФИО, посмотреть свои записи и историю записей;

<b>{master_main_menu_buttons[0]}</b> – здесь можно посмотреть свои рабочие смены и записи клиентов;

<b>{master_main_menu_buttons[1]}</b> – здесь можно узнать, на сколько баллов клиенты оценили качество услуг;

<b>{toggle_role_buttons[0]}</b> – кнопка переключения с Меню мастера (активное) на Меню клиента;

'''

master_ratings_buttons = ('last_work_day_button', 'date_ratings_button')


def get_master_ratings_keyboard():
    '''Клавиатура оценок мастера'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text='Выбрать дату', callback_data=master_ratings_buttons[1])],
        [types.InlineKeyboardButton(
            text='Прошлая смена', callback_data=master_ratings_buttons[0]),],
    ])
    return keyboard
