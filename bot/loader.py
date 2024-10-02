import logging
import pathlib

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from decouple import config

path = pathlib.Path().absolute()
bot = Bot(token=config('TOKEN'), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
