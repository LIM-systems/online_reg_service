import os

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from bot.db_reqs import client as db_client
from bot.loader import router
from bot.utils.keyboards.client import loyality_programm_buttons
from bot.utils.states.StateClientProfile import ListOfLoayalityProgramm
from online_reg_bot.settings.base import BASE_DIR


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
