import asyncio
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils import exceptions

from filters import IsGroup
from handlers.users.archive import ADMIN_S
from keyboards.default.menuKeyboard import menu_admin, back
from loader import dp, db
from states import Personaldata


@dp.message_handler(IsGroup(), text="📧 Reklama yuborish")
async def add_market(message: types.Message):
    if message.from_user.id in ADMIN_S:
        await message.answer("Reklama xabarnomasini yuboring...", reply_markup=back)
        await Personaldata.Market.media.set()


@dp.message_handler(state=Personaldata.Market.media, content_types=types.ContentType.ANY)
async def send_bax(message: types.Message, state: FSMContext):
    senders = await db.count_users_one()
    await state.finish()
    await message.reply("Xabar yuborish boshlandi !", reply_markup=menu_admin)
    for sender in senders:
        try:
            await dp.bot.copy_message(chat_id=int(sender['telegram_id']), from_chat_id=message.chat.id,
                                      message_id=message.message_id)
            await asyncio.sleep(0.8)
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")
        except Exception as err:
            logging.error(f"All error: {err}")



@dp.message_handler(state=Personaldata.Market.media, text="🔙 Orqaga")
async def back_key_market(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_S:
        await message.answer("Bosh menyu", reply_markup=menu_admin)
        await state.finish()
