import ast
import asyncio
import logging

import aiogram
from aiogram.dispatcher import FSMContext
import aiohttp
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import exceptions

from data.config import CHECKER_ADMIN, SEND_CHANNELS
from handlers.users.vocabulary_words import acceptance_text, limit_photo, keyword_photo_name, anime, anime_grap, \
    no_photo
from loader import dp, db
from states import Personaldata


@dp.message_handler(state=Personaldata.PersonalPhoto.photo, content_types=types.ContentType.PHOTO)
async def done_photo(message: types.Message):
    try:
        arxiv = await dp.bot.send_photo(chat_id=-1001700284640, photo=message.photo[-1].file_id)
        photo_url = f'https://t.me/bsbsi390000000idjdjxj/{arxiv.message_id}'
        language_request_input_photo = await db.select_users_one(telegram_id=message.chat.id)
        string_list_request = language_request_input_photo["photo"]
        result_list_request = ast.literal_eval(string_list_request)
        result_list_request.append(photo_url)
        await db.update_photo(photo=f"{result_list_request}", telegram_id=message.chat.id)
    except Exception as err:
        logging.error(f"ChatNotFound error: {err}")



async def download_photo(photo: types.PhotoSize) -> str:
    file = await photo.download()
    return file.name


async def download_video(video: types.Video) -> str:
    try:
        file_vide = await video.download()
        return file_vide.name
    except:
        file_vide = await video.download()
        return file_vide.name


async def upload_image_to_telegraph(file_path):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file', open(file_path, 'rb'))
        async with session.post('https://telegra.ph/upload', data=data) as response:
            if response.status == 200:
                response_data = await response.json()
                img_url = f'https://telegra.ph{response_data[0]["src"]}'
                return img_url
            else:
                return None


@dp.message_handler(state=Personaldata.PersonalPhoto.photo, text=['🗳 Отправить', '🗳 Yuborish'])
async def acceptance_images(message: types.Message, state: FSMContext):
    language_request_acceptance = await db.select_users_one(telegram_id=message.chat.id)
    string_list_acceptance = language_request_acceptance["photo"]
    result_list_acceptance = ast.literal_eval(string_list_acceptance)
    if len(result_list_acceptance) >= 6:
        anime_id = await message.answer(text=f"{anime[language_request_acceptance['language_db']]}□□□□□□□□□□ 0%")
        await asyncio.sleep(0.5)
        for anm in anime_grap:
            new_message = await dp.bot.edit_message_text(chat_id=message.chat.id,
                                                         message_id=anime_id.message_id,
                                                         text=f"{anime[language_request_acceptance['language_db']]}{anm}")
            anime_id = new_message
            await asyncio.sleep(0.2)
        await anime_id.delete()
        await message.answer(text=acceptance_text[language_request_acceptance['language_db']],
                             reply_markup=types.ReplyKeyboardRemove())
        album = types.MediaGroup()
        for number, media in enumerate(result_list_acceptance):
            if media == result_list_acceptance[-1]:
                album.attach_photo(photo=media, caption=language_request_acceptance['name_db'])
            else:
                album.attach_photo(photo=media)
            if number == 9:
                break

        for channel in SEND_CHANNELS:
            try:
                await dp.bot.send_message(chat_id=channel, text="<b>YANGI NOMZOD👇🏻</b>")
                try:
                    await dp.bot.send_media_group(chat_id=channel, media=album)
                except aiogram.utils.exceptions.RetryAfter:
                    await asyncio.sleep(8)
                    await dp.bot.send_media_group(chat_id=channel, media=album)

                if language_request_acceptance['telegram'] is None:
                    Telegram = f"{message.from_user.get_mention(as_html=True)}"
                else:
                    Telegram = language_request_acceptance['telegram']
                if language_request_acceptance['gender'] == 'woman':
                    await dp.bot.send_message(chat_id=channel,
                                              text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                                   f"<b>Yo'nalish:</b> {language_request_acceptance['species']}\n"
                                                   f"<b>Jinsi:</b> 👱🏻‍♀️Ayol/qiz\n"
                                                   f"•<b>F.I.O:</b> {language_request_acceptance['name_db']}\n"
                                                   f"•<b>Viloyati:</b> {language_request_acceptance['city']}\n"
                                                   f"•<b>Millati:</b> {language_request_acceptance['nationality']}\n"
                                                   f"•<b>Tug'ilgan kuni:</b> {language_request_acceptance['birthday']}\n"
                                                   f"•<b>Yoshi:</b> {language_request_acceptance['age']}\n"
                                                   f"•<b>Balandligi(sm):</b> {language_request_acceptance['height_length']}\n"
                                                   f"•<b>Sochning rangi:</b> {language_request_acceptance['hair_color']}\n"
                                                   f"•<b>Ko'z rangi:</b> {language_request_acceptance['eye_color']}\n"
                                                   f"•<b>Kiyim o'lchami:</b> {language_request_acceptance['dress_size']}\n"
                                                   f"•<b>Oyoq kiyim:</b> {language_request_acceptance['footwear_size']}\n"
                                                   f"•<b>Ko'krak(sm):</b> {language_request_acceptance['breast_size']}\n"
                                                   f"•<b>Bel(sm):</b> {language_request_acceptance['waist_size']}\n"
                                                   f"•<b>Oyoqning son qismi(sm):</b> {language_request_acceptance['footless_size']}\n"
                                                   f"•<b>E-mail:</b> {language_request_acceptance['email']}\n"
                                                   f"•<b>Telefon:</b> {language_request_acceptance['phone_number']}\n"
                                                   f"•<b>Telegram:</b> {Telegram}\n"
                                                   f"•<b>Facebook:</b> {language_request_acceptance['facebook']}\n"
                                                   f"•<b>Instagram:</b> {language_request_acceptance['instagram']}")
                else:
                    await dp.bot.send_message(chat_id=channel,
                                              text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                                   f"<b>Yo'nalish:</b> {language_request_acceptance['species']}\n"
                                                   f"<b>Jinsi:</b> 👨🏻Erkak\n"
                                                   f"•<b>F.I.O:</b> {language_request_acceptance['name_db']}\n"
                                                   f"•<b>Viloyati:</b> {language_request_acceptance['city']}\n"
                                                   f"•<b>Millati:</b> {language_request_acceptance['nationality']}\n"
                                                   f"•<b>Tug'ilgan kuni:</b> {language_request_acceptance['birthday']}\n"
                                                   f"•<b>Yoshi:</b> {language_request_acceptance['age']}\n"
                                                   f"•<b>Balandligi(sm):</b> {language_request_acceptance['height_length']}\n"
                                                   f"•<b>Sochning rangi:</b> {language_request_acceptance['hair_color']}\n"
                                                   f"•<b>Ko'z rangi:</b> {language_request_acceptance['eye_color']}\n"
                                                   f"•<b>Kiyim o'lchami:</b> {language_request_acceptance['dress_size']}\n"
                                                   f"•<b>Oyoq kiyim:</b> {language_request_acceptance['footwear_size']}\n"
                                                   f"•<b>E-mail:</b> {language_request_acceptance['email']}\n"
                                                   f"•<b>Telefon:</b> {language_request_acceptance['phone_number']}\n"
                                                   f"•<b>Telegram:</b> {Telegram}\n"
                                                   f"•<b>Facebook:</b> {language_request_acceptance['facebook']}\n"
                                                   f"•<b>Instagram:</b> {language_request_acceptance['instagram']}")
            except exceptions.ChatNotFound as e:
                logging.error(f"ChatNotFound error: {e}")
            await asyncio.sleep(1)

        inline_keyboard_acceptance_images = InlineKeyboardMarkup(row_width=2)
        inline_uz6_1 = InlineKeyboardButton(f"⛔️Rad etish",
                                            callback_data="not")
        inline_uz6_2 = InlineKeyboardButton(f"🟢Qabul qilish",
                                            callback_data="done")
        inline_uz6_3 = InlineKeyboardButton(f"🎁Qabul qilish va 50% chegirma",
                                            callback_data="tips")
        inline_keyboard_acceptance_images.add(inline_uz6_1, inline_uz6_2, inline_uz6_3)
        for checker in CHECKER_ADMIN:
            try:
                media_message = await dp.bot.send_media_group(chat_id=checker, media=album)
                if language_request_acceptance['telegram'] is None:
                    Telegram = f"{message.from_user.get_mention(as_html=True)}"
                else:
                    Telegram = language_request_acceptance['telegram']
                if language_request_acceptance['gender'] == 'woman':
                    message_ids = await dp.bot.send_message(chat_id=checker,
                                                            text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                                                 f"<b>Yo'nalish:</b> {language_request_acceptance['species']}\n"
                                                                 f"<b>Jinsi:</b> 👱🏻‍♀️Ayol/qiz\n"
                                                                 f"•<b>F.I.O:</b> {language_request_acceptance['name_db']}\n"
                                                                 f"•<b>Viloyati:</b> {language_request_acceptance['city']}\n"
                                                                 f"•<b>Millati:</b> {language_request_acceptance['nationality']}\n"
                                                                 f"•<b>Tug'ilgan kuni:</b> {language_request_acceptance['birthday']}\n"
                                                                 f"•<b>Yoshi:</b> {language_request_acceptance['age']}\n"
                                                                 f"•<b>Balandligi(sm):</b> {language_request_acceptance['height_length']}\n"
                                                                 f"•<b>Sochning rangi:</b> {language_request_acceptance['hair_color']}\n"
                                                                 f"•<b>Ko'z rangi:</b> {language_request_acceptance['eye_color']}\n"
                                                                 f"•<b>Kiyim o'lchami:</b> {language_request_acceptance['dress_size']}\n"
                                                                 f"•<b>Oyoq kiyim:</b> {language_request_acceptance['footwear_size']}\n"
                                                                 f"•<b>Ko'krak(sm):</b> {language_request_acceptance['breast_size']}\n"
                                                                 f"•<b>Bel(sm):</b> {language_request_acceptance['waist_size']}\n"
                                                                 f"•<b>Oyoqning son qismi(sm):</b> {language_request_acceptance['footless_size']}\n"
                                                                 f"•<b>E-mail:</b> {language_request_acceptance['email']}\n"
                                                                 f"•<b>Telefon:</b> {language_request_acceptance['phone_number']}\n"
                                                                 f"•<b>Telegram:</b> {Telegram}\n"
                                                                 f"•<b>Facebook:</b> {language_request_acceptance['facebook']}\n"
                                                                 f"•<b>Instagram:</b> {language_request_acceptance['instagram']}",
                                                            reply_markup=inline_keyboard_acceptance_images)
                else:
                    message_ids = await dp.bot.send_message(chat_id=checker,
                                                            text=f"<b>Nomzod haqida ma'limot:</b>\n"
                                                                 f"<b>Yo'nalish:</b> {language_request_acceptance['species']}\n"
                                                                 f"<b>Jinsi:</b> 👨🏻Erkak\n"
                                                                 f"•<b>F.I.O:</b> {language_request_acceptance['name_db']}\n"
                                                                 f"•<b>Viloyati:</b> {language_request_acceptance['city']}\n"
                                                                 f"•<b>Millati:</b> {language_request_acceptance['nationality']}\n"
                                                                 f"•<b>Tug'ilgan kuni:</b> {language_request_acceptance['birthday']}\n"
                                                                 f"•<b>Yoshi:</b> {language_request_acceptance['age']}\n"
                                                                 f"•<b>Balandligi(sm):</b> {language_request_acceptance['height_length']}\n"
                                                                 f"•<b>Sochning rangi:</b> {language_request_acceptance['hair_color']}\n"
                                                                 f"•<b>Ko'z rangi:</b> {language_request_acceptance['eye_color']}\n"
                                                                 f"•<b>Kiyim o'lchami:</b> {language_request_acceptance['dress_size']}\n"
                                                                 f"•<b>Oyoq kiyim:</b> {language_request_acceptance['footwear_size']}\n"
                                                                 f"•<b>E-mail:</b> {language_request_acceptance['email']}\n"
                                                                 f"•<b>Telefon:</b> {language_request_acceptance['phone_number']}\n"
                                                                 f"•<b>Telegram:</b> {Telegram}\n"
                                                                 f"•<b>Facebook:</b> {language_request_acceptance['facebook']}\n"
                                                                 f"•<b>Instagram:</b> {language_request_acceptance['instagram']}",
                                                            reply_markup=inline_keyboard_acceptance_images)
                photo_s = []
                for list_in in media_message:
                    photo_s.append(list_in.message_id)
                await db.add_data_message(message_id=message_ids.message_id,
                                          telegram_id=message.chat.id,
                                          photo_id=f'{photo_s}',
                                          chat_id=int(checker))
            except exceptions.ChatNotFound as e:
                logging.error(f"ChatNotFound error: {e}")
            await asyncio.sleep(1)
        await state.finish()
    else:
        inline_keyboard_photo2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        inline_uz42 = KeyboardButton(f"{keyword_photo_name[language_request_acceptance['language_db']]}")
        inline_keyboard_photo2.add(inline_uz42)
        await message.answer(text=f"{limit_photo[language_request_acceptance['language_db']]}"
                                  f"{len(result_list_acceptance)}",
                             reply_markup=inline_keyboard_photo2)
