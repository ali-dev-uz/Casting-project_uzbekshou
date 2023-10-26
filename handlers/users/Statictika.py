from aiogram import types

from filters import IsGroup
from handlers.users.archive import CHANNELS
from loader import dp, db


@dp.message_handler(IsGroup(), text="📊 Statistika")
async def finish(message: types.Message):
    members = await db.count_users()
    server_data = await db.select_static_one(data_id=1)
    await message.answer(f"<b>👥 Obunachilar:</b> {members} ta\n"
                         f"<b>➕ Kunlik qo'shilishlar:</b> {server_data['days']} ta\n"
                         f"<b>➕ Haftalik qo'shilishlar:</b> {server_data['weekly']} ta\n"
                         f"<b>➕ Oylik qo'shilishlar: </b> {server_data['monthly']} ta")


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
