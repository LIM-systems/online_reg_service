from aiogram import types

from bot.db_reqs import common as db_common


# кнопки главного меню
# клиент
client_main_menu_buttons = ('👥 О нас', '👔 Чат с менеджером',
                            '📬 Программа лояльности', '📘 Записаться')

# мастер
master_main_menu_buttons = ('📘 Мой график', '📫Мои оценки',)

# админ
admin_main_menu_buttons = ('Рассылка', 'Админка',)


# мой профиль
my_profile_button = '💎 Мой профиль'
my_profile_buttons = ('name_profile_button', 'phone_profile_button',
                      'email_profile_button',)

# кнопка записей клиента
my_profile_client_buttons = (*my_profile_buttons, 'my_entries_profile_button')


def my_profile_keyboard(role='client'):
    '''Главная клавиатура клиента'''
    kb = [
        [types.InlineKeyboardButton(
            text='Имя', callback_data=my_profile_client_buttons[0]),
            types.InlineKeyboardButton(
            text='Телефон', callback_data=my_profile_client_buttons[1])],
        [types.InlineKeyboardButton(
            text='Email', callback_data=my_profile_client_buttons[2]),],
    ]
    if role == 'client':
        kb[1].append(types.InlineKeyboardButton(
            text='Мои записи', callback_data=my_profile_client_buttons[3]))
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def text_my_profile(user_data, role='client'):
    '''Текст для меню профиля'''
    text = f'''Мой профиль

🔹Имя: {user_data.name}
🔹Номер телефона: {user_data.phone}
🔹Email: {user_data.email}

'''
    if role == 'client':
        text += 'Выберите данные, которые хотите изменить, или <i>"Мои записи"</i>, чтобы посмотреть журнал записей.'
    return text


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


# переключение ролей
toggle_role_buttons = ('💁🏻‍♂️Меню клиента',
                       'Меню мастера', 'Меню админа')


async def get_roles(tg_id):
    '''Получить роли'''

    db_roles = await db_common.check_roles(tg_id)
    roles = [role for role in db_roles]
    master, admin = roles
    role = 'client'
    if admin and admin.is_active_role:
        role = 'admin'
    elif master and master.is_active_role:
        role = 'master'

    roles = {
        'active': role,
        'exists': {
            'master': master,
            'admin': admin
        }
    }

    return roles
