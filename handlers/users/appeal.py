import pprint

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from handlers.users.vocabulary_words import types_direction, casting_text, species_keyword, keyword_info, \
    keyword_info_2, keyword_photo_name
from loader import dp, db
from states import Personaldata
import json


@dp.callback_query_handler(state=Personaldata.Welcome.wel, text=[0, 1, 2, 3, 4, 5])
async def done_species(call: types.CallbackQuery, state: FSMContext):
    call_message = call
    await call.message.delete()
    for check_i, check_v in enumerate(types_direction["uz"]):
        if check_i == int(call_message.data):
            await db.update_species(species=check_v, telegram_id=call_message.message.chat.id)
    inline_keyboard_species = InlineKeyboardMarkup(row_width=2)
    language_species = await db.select_users_one(telegram_id=call_message.message.chat.id)
    inline_uz2 = InlineKeyboardButton(f"{species_keyword[language_species['language_db']]}",
                                      callback_data="next")
    inline_keyboard_species.add(inline_uz2)
    await call.message.answer(text=casting_text[language_species['language_db']], reply_markup=inline_keyboard_species)
    await state.finish()


@dp.callback_query_handler(text=["next"])
async def done_species_next(call: types.CallbackQuery):
    call_next = call
    await call.message.delete()
    language_next = await db.select_users_one(telegram_id=call_next.message.chat.id)
    inline_keyboard_next = ReplyKeyboardMarkup(resize_keyboard=True)
    if language_next['language_db'] == "uz":
        inline_uz3 = KeyboardButton("📝 Anketa",
                                    web_app=WebAppInfo(
                                        url='https://dynamic-d000000affodil-aeb0a9.netlify.app/'))
    else:
        inline_uz3 = KeyboardButton("📝 Анкета",
                                    web_app=WebAppInfo(
                                        url='https://prismatic-p00000000000egasus-aca2f3.netlify.app/'))
    inline_keyboard_next.add(inline_uz3)
    await call.message.answer(text=keyword_info[language_next['language_db']], reply_markup=inline_keyboard_next)
    await Personaldata.PersonalInfo.info.set()


@dp.message_handler(content_types=['web_app_data'], state=Personaldata.PersonalInfo.info)
async def web_app(message: types.Message):
    data_output = json.loads(message.web_app_data.data)
    try:
        if data_output['gender'] == 'man':

            if data_output['manTelegram'] == '':
                Telegram = None
            else:
                Telegram = data_output['manTelegram']
            if data_output['manInstagram'] == '':
                Instagram = None
            else:
                Instagram = data_output['manInstagram']
            if data_output['manFacebook'] == '':
                Facebook = None
            else:
                Facebook = data_output['manFacebook']
            await db.update_all(name_db=data_output['manName'],
                                city=data_output['manCity'],
                                nationality=data_output['manNationality'],
                                birthday=data_output['manBirthdate'],
                                age=int(data_output['manAge']),
                                height_length=data_output['manHeight'],
                                hair_color=data_output['manHairColor'],
                                eye_color=data_output['manEyeColor'],
                                dress_size=data_output['manClothingSize'],
                                footwear_size=data_output['manShoeSize'],
                                email=data_output['manEmail'],
                                phone_number=data_output['manPhoneNumber'],
                                telegram=Telegram,
                                facebook=Facebook,
                                instagram=Instagram,
                                breast_size=None,
                                waist_size=None,
                                footless_size=None,
                                gender=data_output['gender'],
                                telegram_id=message.chat.id)
        elif data_output['gender'] == 'woman':
            if data_output['womanTelegram'] == '':
                Telegram = None
            else:
                Telegram = data_output['womanTelegram']
            if data_output['womanInstagram'] == '':
                Instagram = None
            else:
                Instagram = data_output['womanInstagram']
            if data_output['womanFacebook'] == '':
                Facebook = None
            else:
                Facebook = data_output['womanFacebook']
            await db.update_all(name_db=data_output['womanName'],
                                city=data_output['womanCity'],
                                nationality=data_output['womanNationality'],
                                birthday=data_output['womanBirthdate'],
                                age=int(data_output['womanAge']),
                                height_length=data_output['womanHeight'],
                                hair_color=data_output['womanHairColor'],
                                eye_color=data_output['womanEyeColor'],
                                dress_size=data_output['womanClothingSize'],
                                footwear_size=data_output['womanShoeSize'],
                                email=data_output['womanEmail'],
                                phone_number=data_output['womanPhoneNumber'],
                                telegram=Telegram,
                                facebook=Facebook,
                                instagram=Instagram,
                                breast_size=data_output['womanKokrak'],
                                waist_size=data_output['womanWaistType'],
                                footless_size=data_output['womanChestType'],
                                gender=data_output['gender'],
                                telegram_id=message.chat.id)
    except Exception as e:
        await dp.bot.send_message(chat_id=5397857416, text=f"Error web app: {e}")
    language_web = await db.select_users_one(telegram_id=message.chat.id)
    inline_keyboard_photo = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    inline_uz4 = KeyboardButton(f"{keyword_photo_name[language_web['language_db']]}")
    inline_keyboard_photo.add(inline_uz4)
    await message.answer(text=keyword_info_2[language_web['language_db']], reply_markup=inline_keyboard_photo)
    await Personaldata.PersonalPhoto.photo.set()


