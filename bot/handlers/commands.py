import re

from aiogram import F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from bot.db_reqs import common as db_common
from bot.loader import router
from bot.utils.keyboards import (get_name_keyboard, get_phone_keyboard,
                                 sign_up_button, start_keyboard)
from bot.utils.StateSignUp import SignUp
from utils.other import email_pattern, send_verification_email


# вход и регистрация
@router.message(Command('start'), StateFilter('*'))
async def start_handler(msg: types.Message, state: FSMContext):
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
        pass


@router.message(StateFilter(SignUp.first_buttons), F.text == sign_up_button)
async def sign_in_button_handler(msg: types.Message, state: FSMContext):
    '''Обработчик кнопки "Зарегистрироваться"'''
    keyboard = get_name_keyboard(msg.from_user.full_name)
    await msg.answer('Напишите Ваше имя или используйте, указанное в профиле телеграма.',
                     reply_markup=keyboard)
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
        await state.update_data(email=email)
        code = await send_verification_email(email)
        await state.update_data(verify_code=code)
        await msg.answer('Введите проверочный код, отправленный на Ваш email')
        await state.set_state(SignUp.verify_code)
    else:
        await msg.answer('Неверный формат email. Попробуйте еще раз.')


@router.message(StateFilter(SignUp.verify_code))
async def verify_code_handler(msg: types.Message, state: FSMContext):
    '''Обработчик ввода проверочного кода'''
    data = await state.get_data()
    verification_code = data.get('verify_code')
    if msg.text == verification_code:
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        tg_id = msg.chat.id
        await db_common.sign_up(tg_id, name, phone, email)
        await msg.answer('Регистрация прошла успешно!')
        await state.clear()
    else:
        await msg.answer('Неверный проверочный код. Попробуйте еще раз.')
