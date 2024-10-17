from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.loader import router
from bot.utils.keyboards.client import (send_message_to_manager_buttons,
                                        send_message_to_manager_keyboard)
from bot.utils.states.StateClientProfile import ChatWithManager


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
