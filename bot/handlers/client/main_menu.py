import os

from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from bot.db_reqs import client as db_client
from bot.loader import router
from bot.utils.keyboards.client import about_us_button
from online_reg_bot.settings.base import BASE_DIR


@router.message(F.text == about_us_button)
async def about_us(msg: types.Message, state: FSMContext):
    '''Обработчик кнопки "Войти"'''
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
