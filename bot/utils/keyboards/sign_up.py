from aiogram import types

# начальная клавитатура для неавторизованных
sign_in_button = 'Войти'
sign_up_button = 'Зарегистрироваться'


def start_keyboard():
    '''Клавиатура для неавторизованных пользователей'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text=sign_in_button),
                                                    types.KeyboardButton(text=sign_up_button)]])
    return keyboard


def get_name_keyboard(name):
    '''Кнопка получить имя пользователя из данных телеграма'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text=name)]])
    return keyboard


def get_phone_keyboard():
    '''Кнопка получить номер телефона из данных телеграма'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         keyboard=[[types.KeyboardButton(text='Отправить номер телефона',
                                                                         request_contact=True)]])
    return keyboard
