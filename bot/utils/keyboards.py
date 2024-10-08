import re
from aiogram import types

# начальная клавитатура для неавторизованных
sign_in_button = 'Войти'
sign_up_button = 'Зарегистрироваться'


def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text=sign_in_button),
                                                    types.KeyboardButton(text=sign_up_button)]])
    return keyboard
# sign_in_inline_button = types.InlineKeyboardButton(
#     text='Войти', callback_data='sign_in_button')
# sign_up_inline_button = types.InlineKeyboardButton(
#     text='Зарегистрироваться', callback_data='sign_up_button')
# sign_in_inline_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
#     [
#         sign_in_inline_button,
#         sign_up_inline_button,
#     ]
# ])


# получить имя пользователя
def get_name_keyboard(name):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text=name)]])
    return keyboard


# получить номер телефона пользователя
def get_phone_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text='Отправить номер телефона',
                                                                         request_contact=True)]])
    return keyboard
