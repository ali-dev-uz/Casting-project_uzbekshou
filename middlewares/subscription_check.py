from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.users.Statictika import membership
from handlers.users.archive import ADMIN_S
from loader import dp


class INVESTIGATION(BaseMiddleware):
    async def on_pre_process_update(self, msg: types.Update, data: dict):
        if msg.message:
            user_id = msg.message.from_user.id
        elif msg.callback_query:
            user_id = msg.callback_query.from_user.id
        else:
            return
        try:
            consequent = await membership(user_id=user_id)
            if not consequent:
                pass
            else:
                if user_id in ADMIN_S:
                    pass
                else:
                    keyboard_channel = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
                    for no_channel_info in consequent:
                        try:
                            if str(no_channel_info[:6]) == 'https:':
                                try:
                                    channel_link = InlineKeyboardButton("📢 Obuna bo'lish",
                                                                        url=f"{no_channel_info}")
                                    keyboard_channel.add(channel_link)
                                except:
                                    pass
                        except:
                            try:
                                info = await dp.bot.get_chat(chat_id=no_channel_info)
                                channel_link = InlineKeyboardButton("📢 Obuna bo'lish",
                                                                    url=f"{info.invite_link}")
                                keyboard_channel.add(channel_link)
                            except:
                                pass
                    channel_link = InlineKeyboardButton("✅ Tekshirish", callback_data="tekshirish")
                    keyboard_channel.add(channel_link)
                    await dp.bot.send_message(chat_id=user_id,
                                              text=
                                              "<b>❌ Kechirasiz botimizdan foydalanishdan oldin ushbu kanallarga a'zo bo'lishingiz kerak.</b>",
                                              reply_markup=keyboard_channel)
                raise CancelHandler()

        except EOFError:
            pass
