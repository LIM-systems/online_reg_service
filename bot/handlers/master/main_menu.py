from aiogram import F, types

from bot.loader import router
from bot.utils.keyboards.common import master_main_menu_buttons
from bot.utils.keyboards.master import get_master_ratings_keyboard


### Мои оценки ###
@router.message(F.text == master_main_menu_buttons[1])
async def master_ratings(msg: types.Message):
    '''Посмотреть оценки от клиентов'''
    await msg.answer('''Ваш средний бал - 4.5
Оценки за сегодня: отсутствуют

''', reply_markup=get_master_ratings_keyboard())
