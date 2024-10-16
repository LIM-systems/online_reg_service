import re
from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.db_reqs import client as db_client
from bot.loader import router
from bot.utils.keyboards.client import (get_client_main_menu,
                                        loyality_programm_texts)
from bot.utils.keyboards.common import (cancel_client_keyboard, change_client_name_keyboard,
                                        client_cancel_name_button, get_role, my_profile_button, my_profile_buttons,
                                        my_profile_keyboard, text_my_profile, use_telegram_name_button)
from bot.utils.states.StateClientProfile import ClientProfile
from utils.other import email_pattern, phone_pattern, send_verification_email


### Мой профиль (для клиента и мастера) ###
@router.message(F.text == my_profile_button)
async def my_profile(msg: types.Message, state: FSMContext):
    '''Кнопка "Мой профиль"'''
    await state.clear()

    role = await get_role(msg.from_user.id)
    client_data = await db_client.get_client_info(msg.chat.id)

    if role == 'client':
        # включение/отключение программы лояльности
        await msg.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
    if role == 'master':
        await msg.answer(text_my_profile(client_data, role=role), reply_markup=my_profile_keyboard(role))


@router.callback_query(lambda call: call.data == my_profile_buttons[0])
async def change_name(call: types.CallbackQuery, state: FSMContext):
    '''Изменить имя'''
    await call.message.delete()
    await call.message.answer('Напишите Ваше имя или используйте, указанное в профиле телеграма.',
                              reply_markup=change_client_name_keyboard(call.from_user.full_name))
    await state.set_state(ClientProfile.name)


@router.message(StateFilter(ClientProfile.name))
async def text_name_handler(msg: types.Message, state: FSMContext):
    '''Обработка написанного имени'''
    await msg.answer('Имя было изменено')
    client_data = await db_client.get_client_info(msg.chat.id, name=msg.text)
    await msg.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
    await state.clear()


@router.callback_query(lambda call: call.data == use_telegram_name_button, StateFilter(ClientProfile.name))
async def button_name_handler(call: types.CallbackQuery, state: FSMContext):
    '''Обработка кнопки выбора имени'''
    await call.message.delete()
    client_data = await db_client.get_client_info(call.message.chat.id, name=call.from_user.full_name)
    await call.message.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
    await state.clear()


@router.callback_query(lambda call: call.data == my_profile_buttons[1])
async def change_phone(call: types.CallbackQuery, state: FSMContext):
    '''Изменить телефон'''
    await call.message.delete()
    await call.message.answer('Введите номер телефона (11 цифр) без пробелов и дополнительных символов в формате: 89998889988',
                              reply_markup=cancel_client_keyboard())
    await state.set_state(ClientProfile.phone)


@router.message(StateFilter(ClientProfile.phone))
async def text_phone_handler(msg: types.Message, state: FSMContext):
    '''Обработка написанного телефона'''
    phone = msg.text
    if re.match(phone_pattern, phone):
        await msg.answer('Телефон был изменён')
        client_data = await db_client.get_client_info(msg.chat.id, phone=msg.text)
        await msg.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
        await state.clear()
    else:
        await msg.answer('Неверный формат номера телефона. Попробуйте еще раз.')


@router.callback_query(lambda call: call.data == my_profile_buttons[2])
async def change_email(call: types.CallbackQuery, state: FSMContext):
    '''Изменить email'''
    await call.message.delete()
    await call.message.answer('Введите Ваш email',
                              reply_markup=cancel_client_keyboard())
    await state.set_state(ClientProfile.email)


@router.message(StateFilter(ClientProfile.email))
async def text_email_handler(msg: types.Message, state: FSMContext):
    '''Обработка написанного email'''
    email = msg.text
    if re.match(email_pattern, email):

        # отправка кода подтверждения
        code = await send_verification_email(email)
        await state.update_data(verify_code=code)

        await state.update_data(email=email)
        await msg.answer('Введите проверочный код, отправленный на Ваш email')
        await state.set_state(ClientProfile.verify_code)
    else:
        await msg.answer('Неверный формат email. Попробуйте еще раз.')


@router.message(StateFilter(ClientProfile.verify_code))
async def verify_code_handler(msg: types.Message, state: FSMContext):
    '''Обработчик ввода проверочного кода'''
    data = await state.get_data()
    verification_code = data.get('verify_code')

    if msg.text == verification_code:
        # все собранные данные клиента
        email = data.get('email')
        await msg.answer('Email был изменён')
        client_data = await db_client.get_client_info(msg.chat.id, email=email)
        await msg.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
        await state.clear()
    else:
        await msg.answer('Неверный проверочный код. Попробуйте еще раз.')


@router.callback_query(lambda call: call.data == client_cancel_name_button,
                       StateFilter(ClientProfile))
async def cancel_edit_client_profile(call: types.CallbackQuery, state: FSMContext):
    '''Отмена редактирования профиля'''
    await call.message.delete()
    client_data = await db_client.get_client_info(call.message.chat.id)
    await call.message.answer(text_my_profile(client_data), reply_markup=my_profile_keyboard())
    await state.clear()
