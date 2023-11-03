import asyncio
import logging

from aiogram import types
from aiogram.utils import exceptions

from loader import dp, db


@dp.channel_post_handler(content_types=['video', 'text', 'photo'])
async def channel_handler(message: types.Message):
    print("keldi")
    if not message.caption:
        pass
    elif message.media_group_id:
        pass
    else:
        senders = await db.count_users_one()
        for sender in senders:
            try:
                await dp.bot.copy_message(chat_id=int(sender['telegram_id']), from_chat_id=message.chat.id,
                                          message_id=message.message_id)
                await asyncio.sleep(0.8)
            except exceptions.ChatNotFound as e:
                logging.error(f"ChatNotFound error: {e}")
            except Exception as err:
                logging.error(f"All error: {err}")
