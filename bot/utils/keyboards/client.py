from aiogram import types
from bot.utils.keyboards.common import client_main_menu_buttons, my_profile_button


def get_client_main_menu(toogle, role_buttons=None):
    '''Клавиатура главного меню клиента'''
    kb = [  # с программой лояльности
        [types.KeyboardButton(text=client_main_menu_buttons[3])],
        [
            types.KeyboardButton(text=my_profile_button),
            types.KeyboardButton(text=client_main_menu_buttons[0])
        ],
        [
            types.KeyboardButton(text=client_main_menu_buttons[2]),
            types.KeyboardButton(text=client_main_menu_buttons[1])
        ]
    ]

    if not toogle:
        kb = [  # без программы лояльности
            [
                types.KeyboardButton(text=client_main_menu_buttons[3]),
                types.KeyboardButton(text=my_profile_button)
            ],
            [
                types.KeyboardButton(text=client_main_menu_buttons[0]),
                types.KeyboardButton(text=client_main_menu_buttons[1])
            ]
        ]

    if role_buttons:  # кнопки переключения ролей
        kb.append(role_buttons)

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text = f'''Вам доступны пункты меню:

<b>{my_profile_button}</b> – здесь можно изменить привязанный телефон и ФИО, посмотреть свои записи и историю записей;

<b>{client_main_menu_buttons[3]}</b> – здесь можно записаться на одну или несколько услуг;

<b>{client_main_menu_buttons[0]}</b> – здесь можно узнать о компании, посмотреть место и часы работы;

<b>{client_main_menu_buttons[1]}</b> – здесь можно быстро связаться с администратором;

'''

promo_menu_text = f'<b>{client_main_menu_buttons[2]}</b> – здесь можно приобрести абонемент и узнать о возможных акциях и скидках'


# кнопки выбора записей
entries_client_buttons = ('past_entries_button', 'future_entries_button')


def select_entries_keyboard():
    '''Клавиатура выбора записей'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text='Предыдущие', callback_data=entries_client_buttons[0])],
        [types.InlineKeyboardButton(
            text='Будущие', callback_data=entries_client_buttons[1])],
    ])
    return keyboard


# кнопки программы лояльности
loyality_programm_buttons = ('promos', 'certificates', 'abonements')

loyality_programm_texts = ('''Программа лояльности была отключена.''',
                           '''Программа лояльности вновь доступна.''')


def loyality_programm_keyboard(loyality_programms):
    '''Клавиатура программы лояльности'''
    promos, certificates, abonements = loyality_programms
    kb = []
    if promos:
        kb.append([types.InlineKeyboardButton(
            text='Акции', callback_data=loyality_programm_buttons[0])])
    if certificates:
        kb.append([types.InlineKeyboardButton(
            text='Сертификаты', callback_data=loyality_programm_buttons[1])])
    if abonements:
        kb.append([types.InlineKeyboardButton(
            text='Абонементы', callback_data=loyality_programm_buttons[2])])
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


# кнопки отправки сообщения менеджеру
send_message_to_manager_buttons = ('send_message_to_manager_button',
                                   'cancel_send_message_to_manager_button')


def send_message_to_manager_keyboard():
    '''Клавиатура отправки сообщения менеджеру'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text='Отправить сообщение', callback_data=send_message_to_manager_buttons[0])],
        [types.InlineKeyboardButton(
            text='Отмена', callback_data=send_message_to_manager_buttons[1])],
    ])
    return keyboard
