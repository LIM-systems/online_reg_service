import asyncio

from aiogram import BaseMiddleware, types

from bot.db_reqs.common import check_promo_on_off, check_roles
from bot.utils.keyboards import client
import bot.handlers
from django.core.management.base import BaseCommand

from bot.loader import bot, dp, router


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
                        data['master'] = bool(master)
                        data['admin'] = bool(admin)
                        data['client'] = not (master or admin)
                    except Exception as e:
                        print(f"Role check failed for user {tg_id}: {e}")

                action = None
                if event and event.text:
                    action = event.text
                elif event.callback_query and event.callback_query.data:
                    action = event.callback_query.data

                # Define which buttons require which roles
                client_buttons = (client.about_us_button, client.chat_with_manager_button,
                                  client.my_profile_button, client.promo_button, client.sign_up_on_service_button)
                master_buttons = ('1', '2')

                if action:
                    if action in client_buttons and not data['client']:
                        return
                    elif action in master_buttons and not data['master']:
                        return

                return await handler(event, data)
        router.message.middleware(PromoAndRoleMiddleware())
        router.callback_query.middleware(PromoAndRoleMiddleware())
        asyncio.run(self.start_bot())
