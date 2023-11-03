import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers.users.archive import ADMIN_S
from handlers.users.start import send_welcome_message
from handlers.users.vocabulary_words import language_choice, welcome, orientation, types_direction
from keyboards.default.menuKeyboard import menu_admin
from loader import dp, db
from states import Personaldata


@dp.message_handler(state=[Personaldata.Welcome.wel, Personaldata.PaymeData.pay_data, Personaldata.PersonalInfo.info, Personaldata.PersonalPhoto.photo], commands=['start'])
async def bot_start3(message: types.Message):
    user_id = message.from_user.id
    try:
        await db.update_user_photo(photo='[]', telegram_id=user_id)
    except Exception as err:
        logging.error(f"All error: {err}")

    if user_id in ADMIN_S:
        await message.answer(
            f"<b>👋 Assalomu alaykum Admin</b>", reply_markup=menu_admin)
    else:
        language_request_welcome = await db.select_users_one(telegram_id=user_id)
        try:
            await message.answer(text="<i>Back</i>",
                                 reply_markup=types.ReplyKeyboardRemove())
            await send_welcome_message(user_id=user_id, locale=language_request_welcome['language_db'])

        except Exception as err:
            # await message.answer(text=welcome[language_request_welcome['language_db']])
            await send_welcome_message(user_id=user_id, locale=language_request_welcome['language_db'])
            logging.error(f"All error: {err}")
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
