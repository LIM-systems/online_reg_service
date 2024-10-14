from aiogram import types
import certifi
from django.template.defaulttags import ifchanged


# кнопки главного меню
client_main_menu_buttons = ('👥 О нас', '👔 Чат с менеджером',
                            '💎 Мой профиль', '📬 Программа лояльности', '📘 Записаться')


messages_loyality_programm = (
    'Программа лояльности стала доступна', 'На данный момент программы лояльности нет')


def get_client_main_menu(toogle):
    '''Клавиатура главного меню клиента'''
    kb = [  # с программой лояльности
        [types.KeyboardButton(text=client_main_menu_buttons[4])],
        [
            types.KeyboardButton(text=client_main_menu_buttons[2]),
            types.KeyboardButton(text=client_main_menu_buttons[0])
        ],
        [
            types.KeyboardButton(text=client_main_menu_buttons[3]),
            types.KeyboardButton(text=client_main_menu_buttons[1])
        ]
    ]

    if not toogle:
        kb = [  # без программы лояльности
            [
                types.KeyboardButton(text=client_main_menu_buttons[4]),
                types.KeyboardButton(text=client_main_menu_buttons[2])
            ],
            [
                types.KeyboardButton(text=client_main_menu_buttons[0]),
                types.KeyboardButton(text=client_main_menu_buttons[1])
            ]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text = f'''Вам доступны пункты меню:

<b>{client_main_menu_buttons[2]}</b> – здесь можно изменить привязанный телефон и ФИО, посмотреть свои записи и историю записей;

<b>{client_main_menu_buttons[4]}</b> – здесь можно записаться на одну или несколько услуг;

<b>{client_main_menu_buttons[0]}</b> – здесь можно узнать о компании, посмотреть место и часы работы;

<b>{client_main_menu_buttons[1]}</b> – здесь можно быстро связаться с администратором;

'''

promo_menu_text = f'<b>{client_main_menu_buttons[3]}</b> – здесь можно приобрести абонемент и узнать о возможных акциях и скидках'


# мой профиль
my_profile_buttons = ('name_client_button', 'phone_client_button',
                      'email_client_button', 'my_entries_client_button')


def my_profile_keyboard():
    '''Главная клавиатура клиента'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text='Имя', callback_data=my_profile_buttons[0]),
            types.InlineKeyboardButton(
            text='Телефон', callback_data=my_profile_buttons[1])],
        [types.InlineKeyboardButton(
            text='Email', callback_data=my_profile_buttons[2]),
            types.InlineKeyboardButton(
            text='Мои записи', callback_data=my_profile_buttons[3])],
    ])
    return keyboard


def client_text_my_profile(client_data):

    return f'''Мой профиль

🔹Имя: {client_data.name}
🔹Номер телефона: {client_data.phone}
🔹Email: {client_data.email}

Выберите данные, которые хотите изменить, или <i>"Мои записи"</i>, чтобы посмотреть журнал записей.
'''


# кнопка отмены
client_cancel_name_button = 'client_cancel_button'
client_cancel_button = types.InlineKeyboardButton(
    text='Отмена', callback_data=client_cancel_name_button)

# кнопка применения имени из телеграм профиля
use_telegram_name_button = 'use_telegram_name_button'


def change_client_name_keyboard(name):
    '''Клавиатура изменение имени клиента'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(
            text=name, callback_data=use_telegram_name_button)],
        [client_cancel_button]
    ])
    return keyboard


def cancel_client_keyboard():
    '''Клавиатура изменение телефона клиента'''
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [client_cancel_button]
    ])
    return keyboard


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
