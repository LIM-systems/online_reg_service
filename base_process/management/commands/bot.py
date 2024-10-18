import asyncio

from aiogram import BaseMiddleware, types
from django.core.management.base import BaseCommand

import bot.handlers
from bot.db_reqs.common import check_promo_on_off, check_roles
from bot.loader import bot, dp, router
from bot.utils.keyboards.master import master_ratings_buttons
from bot.utils.keyboards.common import admin_main_menu_buttons, master_main_menu_buttons
from bot.utils.keyboards.admin import broadcast_buttons


class Command(BaseCommand):
    help = 'Запуск бота'

    async def start_bot(self):
        try:
            await dp.start_polling(bot)
        finally:
            await bot.session.close()

    def handle(self, *args, **options):

        class PromoAndRoleMiddleware(BaseMiddleware):
            async def __call__(self, handler, event: types.Update, data: dict):

                # подключение и отключение промо
                try:
                    promo_active = await check_promo_on_off()
                    data['promo_active'] = promo_active
                except Exception as e:
                    print(e)
                    data['promo_active'] = False

                # доступ ролей
                data['master'] = False
                data['admin'] = False
                data['client'] = False

                tg_id = None
                if event:
                    tg_id = event.from_user.id
                elif event.callback_query:
                    tg_id = event.callback_query.from_user.id

                if tg_id:
                    try:
                        master, admin = await check_roles(tg_id)
                        data['admin'] = bool(admin and admin.is_active_role)
                        data['master'] = bool(master and master.is_active_role)
                        data['client'] = not (
                            data['master'] or data['admin'])
                    except Exception as e:
                        print(f"Role check failed for user {tg_id}: {e}")

                action = None
                if isinstance(event, types.Message) and event.text:
                    action = event.text
                elif isinstance(event, types.CallbackQuery) and event.data:
                    action = event.data

                master_buttons = (*master_ratings_buttons,
                                  *master_main_menu_buttons)
                admin_buttons = (*admin_main_menu_buttons, *broadcast_buttons)

                if action:
                    if data['client'] and action in master_buttons\
                            or action in admin_buttons:
                        return
                    if data['master'] and action in admin_buttons:
                        return

                return await handler(event, data)
        router.message.middleware(PromoAndRoleMiddleware())
        router.callback_query.middleware(PromoAndRoleMiddleware())
        asyncio.run(self.start_bot())
