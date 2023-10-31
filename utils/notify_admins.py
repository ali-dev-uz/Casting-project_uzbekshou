import logging

from aiogram.utils import exceptions
from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Bot ishga tushdi")
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")

        except Exception as err:
            logging.exception(err)
