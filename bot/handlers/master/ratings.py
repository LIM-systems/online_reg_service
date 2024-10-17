from aiogram import types

from bot.loader import router
from bot.utils.keyboards.master import master_ratings_buttons


@router.callback_query(lambda call: call.data == master_ratings_buttons[0])
async def show_ratings_last_work_day(call: types.CallbackQuery):
    '''Посмотреть оценки за предыдущий рабочий день'''
    await call.message.delete()
    await call.message.answer('Оценки за предыдущий рабочий день: отсутствуют')


@router.callback_query(lambda call: call.data == master_ratings_buttons[1])
async def show_ratings_selected_date(call: types.CallbackQuery):
    '''Посмотреть оценки за выбранную дату'''
    await call.message.delete()
    await call.message.answer('У Вас ещё не было рабочих дней.')
