import os
import re

from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from bot.db_reqs import client as db_client
from bot.loader import router
from bot.utils.keyboards.client import (cancel_client_keyboard, change_client_name_keyboard,
                                        client_cancel_name_button, client_main_menu_buttons, client_text_my_profile,
                                        entries_client_buttons, loyality_programm_buttons, loyality_programm_keyboard,
                                        my_profile_buttons, my_profile_keyboard, select_entries_keyboard,
                                        send_message_to_manager_buttons, send_message_to_manager_keyboard, use_telegram_name_button)
from bot.utils.states.StateClientProfile import ChatWithManager, ClientProfile, ListOfLoayalityProgramm
from online_reg_bot.settings.base import BASE_DIR
from utils.other import email_pattern, phone_pattern, send_verification_email


### О нас ###
@router.message(F.text == client_main_menu_buttons[0])
async def about_us(msg: types.Message, state: FSMContext):
    '''Кнопка "О нас"'''
    await state.clear()
    about_us_info = await db_client.get_about_us_info()
    image = about_us_info[2]
    message = f'''{about_us_info[0]}

{about_us_info[1]}

Адрес: {about_us_info[3]}
Рабочее дни: {about_us_info[4]}
Рабочее время: {about_us_info[5]}
Телефон: {about_us_info[6]}'''
    if image:
        image_path = os.path.join(
            BASE_DIR, 'media', 'about_company', os.path.basename(image))
        photo = FSInputFile(image_path)
        await msg.answer_photo(photo, caption=message)
    else:
        await msg.answer(message)


### Мой профиль ###
@router.message(F.text == client_main_menu_buttons[2])
async def my_profile(msg: types.Message, state: FSMContext):
    '''Кнопка "Мой профиль"'''
    await state.clear()
    client_data = await db_client.get_client_info(msg.chat.id)
    await msg.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())


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
    await msg.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())
    await state.clear()


@router.callback_query(lambda call: call.data == use_telegram_name_button, StateFilter(ClientProfile.name))
async def button_name_handler(call: types.CallbackQuery, state: FSMContext):
    '''Обработка кнопки выбора имени'''
    await call.message.delete()
    client_data = await db_client.get_client_info(call.message.chat.id, name=call.from_user.full_name)
    await call.message.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())
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
        await msg.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())
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
        await msg.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())
        await state.clear()
    else:
        await msg.answer('Неверный проверочный код. Попробуйте еще раз.')


@router.callback_query(lambda call: call.data == my_profile_buttons[3])
async def select_entries_email(call: types.CallbackQuery):
    '''Выбрать записи'''
    await call.message.delete()
    await call.message.answer('Выберите записи',
                              reply_markup=select_entries_keyboard())


@router.callback_query(lambda call: call.data == entries_client_buttons[0])
async def past_entries(call: types.CallbackQuery):
    '''Отображение прошлых записей'''
    await call.message.answer('У вас пока не было записей.')


@router.callback_query(lambda call: call.data == entries_client_buttons[1])
async def future_entries(call: types.CallbackQuery):
    '''Отображение будущих записей'''
    await call.message.answer('У вас пока не было записей.')


@router.callback_query(lambda call: call.data == entries_client_buttons[1])
async def future_entries(call: types.CallbackQuery):
    '''Отображение будущих записей'''
    await call.message.answer('У вас пока не было записей.')


@router.callback_query(lambda call: call.data == client_cancel_name_button,
                       StateFilter(ClientProfile))
async def cancel_edit_client_profile(call: types.CallbackQuery, state: FSMContext):
    '''Отмена редактирования профиля'''
    await call.message.delete()
    client_data = await db_client.get_client_info(call.message.chat.id)
    await call.message.answer(client_text_my_profile(client_data), reply_markup=my_profile_keyboard())
    await state.clear()


# Программы лояльности ###
@router.message(F.text == client_main_menu_buttons[3])
async def loyality_programm(msg: types.Message):
    '''Кнопка "Программы лояльности"'''
    loyality_programms = await db_client.get_loaylity_programs()
    await msg.answer('Выберите программу лояльности', reply_markup=loyality_programm_keyboard(loyality_programms))


@router.callback_query(lambda call: call.data == loyality_programm_buttons[0])
async def all_promos(call: types.CallbackQuery):
    '''Отображение акций'''
    await call.message.delete()
    loaylity_programs = await db_client.get_loaylity_programs()
    promos = loaylity_programs[0]

    for promo in promos:

        # данные каждой акции
        name = promo.name
        description = promo.description
        image = promo.image
        discount = promo.discount
        start_date = promo.date_start
        end_date = promo.date_end

        # формирование сообщения
        message = name + '\n'
        if description:
            message += '\n' + description
        message += '\n' + f'Скидка {discount}%'
        if start_date:  # преобразуем дату старта в читаемый вид
            formatted_date = start_date.strftime("%d.%m.%Y")
            formatted_time = start_date.strftime("%H:%M")
            message += '\n' + \
                f'С {formatted_date} {formatted_time}'
        if end_date:  # преобразуем дату окончания в читаемый вид
            formatted_date = end_date.strftime("%d.%m.%Y")
            formatted_time = end_date.strftime("%H:%M")
            message += f' по {formatted_date} {formatted_time}'

        # отправка сообщения
        if image:
            image_path = os.path.join(
                BASE_DIR, 'media', 'promotions', os.path.basename(image))
            photo = FSInputFile(image_path)
            await call.message.answer_photo(photo, caption=message)
        else:
            await call.message.answer(message)


@router.callback_query(lambda call: call.data == loyality_programm_buttons[1]
                       or call.data == loyality_programm_buttons[2])
async def all_loaylity_promos(call: types.CallbackQuery, state: FSMContext):
    '''Отображение сертификатов/абонементов'''
    await call.message.delete()
    is_certifficates = True if call.data == loyality_programm_buttons[1] else False
    loaylity_programs = await db_client.get_loaylity_programs()
    loaylity_promos = loaylity_programs[1] if is_certifficates else loaylity_programs[2]
    loaylity_promos_data = []

    message = 'Сертификаты\n'

    counter = 0
    for item in loaylity_promos:
        counter += 1
        # данные каждого сертификата\abonementa
        id = item.id
        name = item.name
        description = item.description
        image = item.image
        period = item.period
        loaylity_promos_data.append({
            'id': id,
            'counter': counter,
        })
        # формирование сообщения
        message = f'{counter}) {name}\n'
        if description:
            message += '\n' + description
        if period:
            message += '\n' + f'Срок действия {period} дней'
            if image:
                image_path = os.path.join(
                    BASE_DIR, 'media', 'promotions', os.path.basename(image))
                photo = FSInputFile(image_path)
                await call.message.answer_photo(photo, caption=message)
            else:
                await call.message.answer(message)
    text = 'сертификат' if is_certifficates else 'абонемент'
    await call.message.answer(f'Напишите порядковый номер {text}а, который хотите приобрести')
    await state.update_data(name=text)
    await state.update_data(loaylity_promos_list=loaylity_promos_data)
    await state.set_state(ListOfLoayalityProgramm.loaylity_promos_list)


@router.message(StateFilter(ListOfLoayalityProgramm.loaylity_promos_list))
async def loaylity_promos_handler(msg: types.Message, state: FSMContext):
    '''Покупка сертификата/абонемента'''
    data = await state.get_data()
    name = data.get('name')
    loaylity_promos_list = data.get('loaylity_promos_list')
    right_number = False
    for item in loaylity_promos_list:
        if str(msg.text) == str(item['counter']):
            # certificate_id = certificate['id']
            right_number = True
            break
    if right_number:
        await msg.answer('Скоро будет доступен к покупке')
        await state.clear()
    else:
        await msg.answer('Вы ввели неверный номер')


### О нас ###
@router.message(F.text == client_main_menu_buttons[1])
async def chat_with_manager(msg: types.Message, state: FSMContext):
    '''Чат с менеджером"'''
    await state.clear()
    await msg.answer('Напишите сообщение')
    await state.set_state(ChatWithManager.chat_with_manager)


@router.message(StateFilter(ChatWithManager.chat_with_manager))
async def get_message(msg: types.Message, state: FSMContext):
    '''Отправка сообщения боту'''
    await msg.answer('Отправить сообщение?', reply_markup=send_message_to_manager_keyboard())
    await state.clear()


@router.callback_query(lambda call: call.data in send_message_to_manager_buttons)
async def send_message_to_manager(call: types.CallbackQuery, state: FSMContext):
    '''Отправка сообщения менеджеру или отмена'''
    await call.message.delete()
    if call.data == send_message_to_manager_buttons[0]:
        await call.message.answer('Сообщение отправлено')
    else:
        await call.message.answer('Отправка отменена')
