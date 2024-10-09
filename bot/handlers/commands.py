import re

from aiogram import F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from bot.db_reqs import common as db_common
from bot.loader import router
from bot.utils.keyboards.client import get_client_main_menu, start_menu_text, promo_menu_text
from bot.utils.keyboards.sign_up import (get_name_keyboard, get_phone_keyboard,
                                         sign_up_button, sign_in_button, start_keyboard)
from bot.utils.StateSignUp import SignUp
from utils.other import email_pattern, send_verification_email


# вход и регистрация
@router.message(Command('start'), StateFilter('*'))
async def start_handler(msg: types.Message, state: FSMContext, promo_active: bool):
    '''Главная команда /start'''
    await state.clear()
    tg_id = msg.chat.id

    # проверяем авторизацию
    is_auth = await db_common.check_authorization(tg_id)
    if not is_auth:
        greeting = await db_common.get_greeting()
        await msg.answer(greeting, reply_markup=start_keyboard())
        await state.set_state(SignUp.first_buttons)
    else:
        # проверяем роли
        master, admin = await db_common.check_roles(tg_id)

        if admin:
            await msg.answer('меню админа')
        elif master:
            await msg.answer('меню мастера')
        else:
            text = start_menu_text if not promo_active else start_menu_text + promo_menu_text
            await msg.answer(text, reply_markup=get_client_main_menu(promo_active))


@router.message(StateFilter(SignUp.first_buttons), F.text == sign_up_button)
async def sign_up_button_handler(msg: types.Message, state: FSMContext):
    '''Обработчик кнопки "Зарегистрироваться"'''
    await state.update_data(on_or_up='up')
    await msg.answer('Напишите Ваше имя или используйте, указанное в профиле телеграма.',
                     reply_markup=get_name_keyboard(msg.from_user.full_name))
    await state.set_state(SignUp.name)


@router.message(StateFilter(SignUp.name))
async def name_handler(msg: types.Message, state: FSMContext):
    '''Обработчик ввода имени'''
    name = msg.text
    await state.update_data(name=name)
    await msg.answer('Введите номер телефона (11 цифр) без пробелов и дополнительных символов, по образцу:89998889988',
                     reply_markup=get_phone_keyboard())
    await state.set_state(SignUp.phone)


@router.message(StateFilter(SignUp.phone))
async def phone_handler(msg: types.Message, state: FSMContext):
    '''Обработчик ввода телефона'''
    phone = msg.contact.phone_number if msg.contact else msg.text
    if re.match(r'^\+7\d{10}$', phone):
        await state.update_data(phone=phone)
        await msg.answer('Введите Ваш email', reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(SignUp.email)
    else:
        await msg.answer('Неверный формат номера телефона. Попробуйте еще раз.')


@router.message(StateFilter(SignUp.email))
async def email_handler(msg: types.Message, state: FSMContext):
    '''Обработчик ввода email'''
    email = msg.text
    if re.match(email_pattern, email):
        data = await state.get_data()
        on_or_up = data.get('on_or_up')  # регистрация или вход

        # обработка входа/ проверка email в бд
        if on_or_up == 'in':
            is_exists = await db_common.check_authorization(email=email)
            if not is_exists:
                await msg.answer('Данный email не найден')
                return

        # отправка кода подтверждения
        code = await send_verification_email(email)
        await state.update_data(verify_code=code)

        await state.update_data(email=email)
        await msg.answer('Введите проверочный код, отправленный на Ваш email')
        await state.set_state(SignUp.verify_code)
    else:
        await msg.answer('Неверный формат email. Попробуйте еще раз.')


@router.message(StateFilter(SignUp.verify_code))
async def verify_code_handler(msg: types.Message, state: FSMContext, promo_active: bool):
    '''Обработчик ввода проверочного кода'''
    data = await state.get_data()
    verification_code = data.get('verify_code')

    if msg.text == verification_code:
        # все собранные данные клиента
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        tg_id = msg.chat.id

        is_exists = await db_common.check_authorization(email=email)
        if is_exists:
            # обновляем/добавляем тг id
            await db_common.refresh_tg_id(email, tg_id)
        else:
            # записываем в бд
            await db_common.sign_up(tg_id, name, phone, email)

        # отображение меню клиента после регистрации
        text = start_menu_text if not promo_active else start_menu_text + promo_menu_text
        await msg.answer(text, reply_markup=get_client_main_menu(promo_active))
        await state.clear()
    else:
        await msg.answer('Неверный проверочный код. Попробуйте еще раз.')


@router.message(StateFilter(SignUp.first_buttons), F.text == sign_in_button)
async def sign_in_button_handler(msg: types.Message, state: FSMContext):
    '''Обработчик кнопки "Войти"'''
    await state.update_data(on_or_up='in')
    await msg.answer('Введите Ваш email', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(SignUp.email)
