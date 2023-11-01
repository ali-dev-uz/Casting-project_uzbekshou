import ast
import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from data.config import PAYME_ID, PAY_USERS
from handlers.users.vocabulary_words import payme_data, pay_data_5, finish_text, finish_text_no_pay, pay_data_5_2
from loader import dp, db
from states import Personaldata
from utils.file_chacker import is_image, is_video


@dp.callback_query_handler(text=['pay'])
async def done_payment_request(call: types.CallbackQuery):
    call_data = call
    await call.message.delete()
    language_request_payme = await db.select_users_one(telegram_id=call_data.message.chat.id)
    await call.message.answer(text=pay_data_5[language_request_payme['language_db']],
                              reply_markup=types.ReplyKeyboardRemove())
    await call.answer(text=pay_data_5_2[language_request_payme['language_db']], show_alert=True)
    await Personaldata.PaymeData.pay_data.set()


@dp.message_handler(content_types=[types.ContentType.VIDEO, types.ContentType.TEXT, types.ContentType.ANIMATION,
                                   types.ContentType.STICKER], state=Personaldata.PaymeData.pay_data)
async def input_images_ignore(message: types.Message):
    language_request_payme_ignore = await db.select_users_one(telegram_id=message.chat.id)
    await message.answer(pay_data_5[language_request_payme_ignore['language_db']])


@dp.message_handler(content_types=types.ContentType.PHOTO, state=Personaldata.PaymeData.pay_data)
async def input_images(message: types.Message, state: FSMContext):
    language_request_payme_check = await db.select_users_one(telegram_id=message.chat.id)
    await message.answer(text=payme_data[language_request_payme_check['language_db']])
    check_payme_button = InlineKeyboardMarkup(row_width=2)
    name_button_inline_1 = InlineKeyboardButton(text="✅", callback_data='done_pay')
    name_button_inline_2 = InlineKeyboardButton(text="❌", callback_data='not_pay')
    check_payme_button.add(name_button_inline_1, name_button_inline_2)
    try:
        admin_msg = await dp.bot.send_photo(chat_id=PAYME_ID,
                                            photo=message.photo[-1].file_id,
                                            caption=f"<b>⏳ TEKSHIRUV UCHUN CHEK KELDI</b>\n"
                                                    f"To'lovchi: {language_request_payme_check['name_db']}",
                                            reply_markup=check_payme_button)
        await db.add_data_message_pay(message_id=admin_msg.message_id,
                                      telegram_id=message.chat.id)
    except exceptions.ChatNotFound as e:
        logging.error(f"ChatNotFound error: {e}")

    await state.finish()


@dp.callback_query_handler(text=['done_pay', 'not_pay'])
async def admin_check_inline_button(call_msg: types.CallbackQuery):
    call = call_msg
    await call_msg.message.delete()
    castings_id = await db.select_message_data_pay(message_id=call.message.message_id)
    language_admin_check_inline_button = await db.select_users_one(telegram_id=castings_id['telegram_id'])
    if call.data == 'done_pay':
        try:
            await dp.bot.send_message(chat_id=castings_id['telegram_id'],
                                      text=finish_text[language_admin_check_inline_button['language_db']])
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")
        string_list_acceptance1 = language_admin_check_inline_button["photo"]
        result_list_acceptance1 = ast.literal_eval(string_list_acceptance1)
        album2 = types.MediaGroup()
        if len(result_list_acceptance1) >= 6:
            for number, media in enumerate(result_list_acceptance1):
                if media == result_list_acceptance1[-1]:
                    album2.attach_photo(photo=media, caption=language_admin_check_inline_button['name_db'])
                else:
                    album2.attach_photo(photo=media)
                if number == 9:
                    break
        try:
            await dp.bot.send_message(chat_id=PAY_USERS, text="<b>YANGI TO'LOV QILGAN NOMZOD👇🏻</b>")
            await dp.bot.send_media_group(chat_id=PAY_USERS, media=album2)
            if language_admin_check_inline_button['telegram'] is None:
                Telegram = f"None"
            else:
                Telegram = language_admin_check_inline_button['telegram']
            if language_admin_check_inline_button['gender'] == 'woman':
                await dp.bot.send_message(chat_id=PAY_USERS,
                                          text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                               f"<b>Yo'nalish:</b> {language_admin_check_inline_button['species']}\n"
                                               f"<b>Jinsi:</b> 👱🏻‍♀️Ayol/qiz\n"
                                               f"•<b>F.I.O:</b> {language_admin_check_inline_button['name_db']}\n"
                                               f"•<b>Viloyati:</b> {language_admin_check_inline_button['city']}\n"
                                               f"•<b>Millati:</b> {language_admin_check_inline_button['nationality']}\n"
                                               f"•<b>Tug'ilgan kuni:</b> {language_admin_check_inline_button['birthday']}\n"
                                               f"•<b>Yoshi:</b> {language_admin_check_inline_button['age']}\n"
                                               f"•<b>Balandligi(sm):</b> {language_admin_check_inline_button['height_length']}\n"
                                               f"•<b>Sochning rangi:</b> {language_admin_check_inline_button['hair_color']}\n"
                                               f"•<b>Ko'z rangi:</b> {language_admin_check_inline_button['eye_color']}\n"
                                               f"•<b>Kiyim o'lchami:</b> {language_admin_check_inline_button['dress_size']}\n"
                                               f"•<b>Oyoq kiyim:</b> {language_admin_check_inline_button['footwear_size']}\n"
                                               f"•<b>Ko'krak(sm):</b> {language_admin_check_inline_button['breast_size']}\n"
                                               f"•<b>Bel(sm):</b> {language_admin_check_inline_button['waist_size']}\n"
                                               f"•<b>Oyoqning son qismi(sm):</b> {language_admin_check_inline_button['footless_size']}\n"
                                               f"•<b>E-mail:</b> {language_admin_check_inline_button['email']}\n"
                                               f"•<b>Telefon:</b> {language_admin_check_inline_button['phone_number']}\n"
                                               f"•<b>Telegram:</b> {Telegram}\n"
                                               f"•<b>Facebook:</b> {language_admin_check_inline_button['facebook']}\n"
                                               f"•<b>Instagram:</b> {language_admin_check_inline_button['instagram']}")
            else:
                await dp.bot.send_message(chat_id=PAY_USERS,
                                          text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                               f"<b>Yo'nalish:</b> {language_admin_check_inline_button['species']}\n"
                                               f"<b>Jinsi:</b> 👨🏻Erkak\n"
                                               f"•<b>F.I.O:</b> {language_admin_check_inline_button['name_db']}\n"
                                               f"•<b>Viloyati:</b> {language_admin_check_inline_button['city']}\n"
                                               f"•<b>Millati:</b> {language_admin_check_inline_button['nationality']}\n"
                                               f"•<b>Tug'ilgan kuni:</b> {language_admin_check_inline_button['birthday']}\n"
                                               f"•<b>Yoshi:</b> {language_admin_check_inline_button['age']}\n"
                                               f"•<b>Balandligi(sm):</b> {language_admin_check_inline_button['height_length']}\n"
                                               f"•<b>Sochning rangi:</b> {language_admin_check_inline_button['hair_color']}\n"
                                               f"•<b>Ko'z rangi:</b> {language_admin_check_inline_button['eye_color']}\n"
                                               f"•<b>Kiyim o'lchami:</b> {language_admin_check_inline_button['dress_size']}\n"
                                               f"•<b>Oyoq kiyim:</b> {language_admin_check_inline_button['footwear_size']}\n"
                                               f"•<b>E-mail:</b> {language_admin_check_inline_button['email']}\n"
                                               f"•<b>Telefon:</b> {language_admin_check_inline_button['phone_number']}\n"
                                               f"•<b>Telegram:</b> {Telegram}\n"
                                               f"•<b>Facebook:</b> {language_admin_check_inline_button['facebook']}\n"
                                               f"•<b>Instagram:</b> {language_admin_check_inline_button['instagram']}")
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")

    elif call.data == 'not_pay':
        try:
            await dp.bot.send_message(chat_id=castings_id['telegram_id'],
                                      text=finish_text_no_pay[language_admin_check_inline_button['language_db']])
        except exceptions.ChatNotFound as e:
            logging.error(f"ChatNotFound error: {e}")

    await db.delete_data_pay(telegram_id=castings_id['telegram_id'])
