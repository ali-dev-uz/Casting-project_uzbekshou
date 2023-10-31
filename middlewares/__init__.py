from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .subscription_check import INVESTIGATION


if __name__ == "middlewares":
    # dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(INVESTIGATION())
