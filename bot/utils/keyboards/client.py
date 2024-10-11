from aiogram import types
import certifi
from django.template.defaulttags import ifchanged


# кнопки главного меню
client_main_menu_buttons = ('О нас', 'Чат с менеджером',
                            'Мой профиль', 'Программы лояльности', 'Записаться')


def get_client_main_menu(toogle):
    kb = [
        [
            types.KeyboardButton(text=client_main_menu_buttons[0]),
            types.KeyboardButton(text=client_main_menu_buttons[1])
        ]
    ]

    # добавлять или нет кнопку промоакций в зависимости от условия
    if toogle:
        kb.append([
            types.KeyboardButton(text=client_main_menu_buttons[2]),
            types.KeyboardButton(text=client_main_menu_buttons[3])
        ])
        kb.append([types.KeyboardButton(text=client_main_menu_buttons[4])])
    else:
        kb.append([
            types.KeyboardButton(text=client_main_menu_buttons[2]),
            types.KeyboardButton(text=client_main_menu_buttons[4])
        ])
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text = '''Вам доступны пункты меню:

💎 Мой профиль – здесь можно изменить привязанный телефон и ФИО, посмотреть свои записи и историю записей;

📘 Записаться – здесь можно записаться на одну или несколько услуг;

👥 О нас – здесь можно узнать о компании, посмотреть место и часы работы;

👔 Чат с менеджером – здесь можно быстро связаться с администратором;


'''

promo_menu_text = '📬 Программа лояльности – здесь можно приобрести абонемент и узнать о возможных акциях и скидках'


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

Имя: {client_data.name}
Номер телефона: {client_data.phone}
Email: {client_data.email}

Выберите "Мои записи" для их просмотра
или данные, которые хотите изменить.
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
