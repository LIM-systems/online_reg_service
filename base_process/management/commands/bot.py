from aiogram import executor
from django.core.management.base import BaseCommand

from bot import handlers
from bot.loader import dp


class Command(BaseCommand):
    help = 'Запись онлайн'

    def handle(self, *args, **options):
        executor.start_polling(dp, skip_updates=False)
