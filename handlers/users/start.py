from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filters import IsGroup
from handlers.users.archive import ADMIN_S
from handlers.users.vocabulary_words import language_choice
from keyboards.default.menuKeyboard import menu_admin
from loader import dp, db


@dp.message_handler(IsGroup(), CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    # if user_id in ADMIN_S:
    #     await message.answer(
    #         f"<b>👋 Assalomu alaykum Admin", reply_markup=menu_admin)
    # else:
    #     await message.answer(
    #         f"<b>👋 Assalomu alaykum {message.from_user.get_mention(as_html=True)}\n"
    #         f"")
    # try:
    #     await db.add_user(telegram_id=message.from_user.id)
    #     global MONTHLY, DAILY, WEEKLY
    #     MONTHLY += 1
    #     DAILY += 1
    #     WEEKLY += 1
    # except:
    #     pass
    await db.add_user(telegram_id=user_id)


async def send_start_lan(user_id):
    language_request = await db.select_users_one(telegram_id=user_id)
    if language_request['language_db'] is None and language_request['language_db'] == "uz":
        inline_keyboard_language = InlineKeyboardMarkup(row_width=2)
        inline_uz = InlineKeyboardButton(f"🇺🇿 O'zbek", callback_data=f"uz")
        inline_ru = InlineKeyboardButton(f'🇷🇺 Rus', callback_data=f"ru")
        inline_keyboard_language.add(inline_uz, inline_ru)
        await dp.bot.send_message(f"<b>{language_choice['uz']}</b>", reply_markup=inline_keyboard_language)
    elif language_request['language_db'] == "ru":
        inline_keyboard_language = InlineKeyboardMarkup(row_width=2)
        inline_uz = InlineKeyboardButton(f"🇺🇿 O'zbek", callback_data=f"uz")
        inline_ru = InlineKeyboardButton(f'🇷🇺 Rus', callback_data=f"ru")
        inline_keyboard_language.add(inline_uz, inline_ru)
        await dp.bot.send_message(f"<b>{language_choice['ru']}</b>", reply_markup=inline_keyboard_language)

