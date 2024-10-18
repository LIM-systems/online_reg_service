from aiogram import F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.loader import router
from bot.utils.keyboards.admin import broadcast_buttons, get_broadcast_keyboard
from bot.utils.states.StateAdminMenu import AdminMenu


@router.message(StateFilter(AdminMenu.message))
async def broadcast_msg_handler(msg: types.Message, state: FSMContext):
    '''Обработчик сообщения с текстом рассылки'''
    await msg.answer('Отправить рассылку?', reply_markup=get_broadcast_keyboard())


@router.callback_query(F.data == broadcast_buttons[0], StateFilter(AdminMenu.message))
async def send_broadcast_msg(call: types.CallbackQuery, state: FSMContext):
    '''Обработчик нажатия на кнопку отправить рассылку'''
    await call.message.edit_text('Рассылка отправлена')
    await state.clear()


@router.callback_query(F.data == broadcast_buttons[1], StateFilter(AdminMenu.message))
async def cancel_broadcast_msg(call: types.CallbackQuery, state: FSMContext):
    '''Обработчик нажатия на кнопку отменить рассылку'''
    await call.message.edit_text('Рассылка отменена')
    await state.clear()
