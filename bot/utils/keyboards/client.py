from aiogram import types


# кнопки
about_us_button = 'О нас'
chat_with_manager_button = 'Чат с менеджером'
my_profile_button = 'Мой профиль'
promo_button = 'Программы лояльности'
sign_up_on_service_button = 'Записаться'


def get_client_main_menu(toogle):
    kb = [
        [
            types.KeyboardButton(text=about_us_button),
            types.KeyboardButton(text=chat_with_manager_button)
        ]
    ]

    # добавлять или нет кнопку промоакций в зависимости от условия
    if toogle:
        kb.append([
            types.KeyboardButton(text=my_profile_button),
            types.KeyboardButton(text=promo_button)
        ])
        kb.append([types.KeyboardButton(text=sign_up_on_service_button)])
    else:
        kb.append([
            types.KeyboardButton(text=my_profile_button),
            types.KeyboardButton(text=sign_up_on_service_button)
        ])
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=kb
    )

    return keyboard


start_menu_text = '''Поздравляем, регистрация прошла успешно. Теперь вам доступны новые пункты меню: 

Мой профиль – здесь можно изменить привязанный номер телефона и ФИО, посмотреть свои записи и историю записей;
Записаться – здесь можно записаться на одну или несколько услуг;
О нас – здесь можно подробнее узнать о компании, посмотреть место и часы работы; 
Чат с менеджером – здесь можно быстро связаться с администратором
'''

promo_menu_text = 'Программа лояльности – здесь можно приобрести абонемент и узнать о возможных акциях и скидках'
