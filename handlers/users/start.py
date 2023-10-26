import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from filters import IsGroup
from handlers.users.archive import ADMIN_S
from handlers.users.vocabulary_words import language_choice, welcome, orientation, types_direction
from keyboards.default.menuKeyboard import menu_admin
from loader import dp, db
from states import Personaldata


# Start qabul qiluvchi handler
@dp.message_handler(IsGroup(), CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.add_data(data_id=1,
                          days=0,
                          weekly=0,
                          monthly=0)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    user_id = message.from_user.id
    try:
        await db.add_user(telegram_id=user_id,
                          language_db=None,
                          name_db=None,
                          city=None,
                          nationality=None,
                          birthday=None,
                          age=None,
                          height_length=None,
                          hair_color=None,
                          eye_color=None,
                          dress_size=None,
                          footless_size=None,
                          footwear_size=None,
                          email=None,
                          phone_number=None,
                          telegram=None,
                          facebook=None,
                          instagram=None,
                          breast_size=None,
                          waist_size=None,
                          species=None)
        await send_start_lan(user_id)
        server_info = await db.select_static_one(data_id=1)
        await db.update_day(days=int(server_info['days']) + 1, data_id=1)
        await db.update_weekly(weekly=int(server_info['weekly']) + 1, data_id=1)
        await db.update_monthly(monthly=int(server_info['monthly']) + 1, data_id=1)
        await Personaldata.Selections.lan.set()
    except asyncpg.exceptions.UniqueViolationError:
        if user_id in ADMIN_S:
            await message.answer(
                f"<b>👋 Assalomu alaykum Admin</b>", reply_markup=menu_admin)
        else:
            language_request_welcome = await db.select_users_one(telegram_id=user_id)
            await message.answer(text=welcome[language_request_welcome['language_db']])
            await orientation_lan(user_id=user_id, locale=language_request_welcome['language_db'])
            await Personaldata.Welcome.wel.set()


async def send_start_lan(user_id):
    language_request = await db.select_users_one(telegram_id=user_id)
    if language_request['language_db'] is None or language_request['language_db'] == "uz":
        inline_keyboard_language = InlineKeyboardMarkup(row_width=2)
        inline_uz = InlineKeyboardButton(f"🇺🇿 O'zbek", callback_data=f"uz")
        inline_ru = InlineKeyboardButton(f'🇷🇺 Rus', callback_data=f"ru")
        inline_keyboard_language.add(inline_uz, inline_ru)
        await dp.bot.send_message(chat_id=user_id, text=f"<b>{language_choice['uz']}</b>", reply_markup=inline_keyboard_language)
    elif language_request['language_db'] == "ru":
        inline_keyboard_language = InlineKeyboardMarkup(row_width=2)
        inline_uz = InlineKeyboardButton(f"🇺🇿 O'zbek", callback_data=f"uz")
        inline_ru = InlineKeyboardButton(f'🇷🇺 Rus', callback_data=f"ru")
        inline_keyboard_language.add(inline_uz, inline_ru)
        await dp.bot.send_message(chat_id=user_id, text=f"<b>{language_choice['ru']}</b>", reply_markup=inline_keyboard_language)


async def orientation_lan(user_id, locale):
    inline_keyboard_orientation = InlineKeyboardMarkup(row_width=2)
    for index_lan, orient in enumerate(types_direction[locale]):
        inline_uz1 = InlineKeyboardButton(f"{orient}", callback_data=f"{index_lan}")
        inline_keyboard_orientation.add(inline_uz1)
    await dp.bot.send_message(chat_id=user_id, text=orientation[locale], reply_markup=inline_keyboard_orientation)
