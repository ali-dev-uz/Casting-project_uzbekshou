from aiogram import types

from filters import IsGroup
from handlers.users.archive import DAILY, WEEKLY, MONTHLY, CHANNELS
from loader import dp, db


@dp.message_handler(IsGroup(), text="📊 Statistika")
async def finish(message: types.Message):
    members = await db.count_users()
    await message.answer(f"<b>👥 Obunachilar:</b> {members} ta\n"
                         f"<b>➕ Kunlik qo'shilishlar:</b> {DAILY} ta\n"
                         f"<b>➕ Haftalik qo'shilishlar:</b> {WEEKLY} ta\n"
                         f"<b>➕ Oylik qo'shilishlar: </b> {MONTHLY} ta")


async def membership(user_id):
    no_members = []
    for channel in CHANNELS:
        try:
            if str(channel[:6]) == 'https:':
                pass
        except:
            try:
                check = await dp.bot.get_chat_member(chat_id=channel, user_id=user_id)
                if check.status == "left":
                    no_members.append(channel)
            except:
                pass

    if not no_members:
        return no_members
    else:
        for channel in CHANNELS:
            try:
                if str(channel[:6]) == 'https:':
                    no_members.append(channel)
            except:
                pass
        return no_members
