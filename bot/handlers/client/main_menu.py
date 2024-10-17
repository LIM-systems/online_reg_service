import os

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from bot.db_reqs import client as db_client
from bot.loader import router
from bot.utils.keyboards.client import (client_main_menu_buttons,
                                        get_client_main_menu,
                                        loyality_programm_keyboard,
                                        loyality_programm_texts,
                                        send_message_to_manager_buttons)
from bot.utils.states.StateClientProfile import ChatWithManager
from online_reg_bot.settings.base import BASE_DIR


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


### Программы лояльности ###
@router.message(F.text == client_main_menu_buttons[2])
async def loyality_programm(msg: types.Message, promo_active: bool):
    '''Кнопка "Программы лояльности"'''
    if not promo_active:
        await msg.answer(loyality_programm_texts[0], reply_markup=get_client_main_menu(promo_active))
        return
    loyality_programms = await db_client.get_loaylity_programs()
    await msg.answer('Выберите программу лояльности', reply_markup=loyality_programm_keyboard(loyality_programms))


### Чат с менеджером ###
@router.message(F.text == client_main_menu_buttons[1])
async def chat_with_manager(msg: types.Message, state: FSMContext, promo_active: bool):
    '''Чат с менеджером'''
    await state.clear()

    kb = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
        text='Отмена', callback_data=send_message_to_manager_buttons[1])]])
    await msg.answer('Напишите сообщение', reply_markup=kb)
    await state.set_state(ChatWithManager.chat_with_manager)
