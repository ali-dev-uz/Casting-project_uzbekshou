from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "<b>This bot was created for the evaluation system</b>"

    await message.answer(text=text)
