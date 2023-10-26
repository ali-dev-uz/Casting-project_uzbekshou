from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import orientation_lan, send_start_lan
from handlers.users.vocabulary_words import welcome
from loader import dp, db
from states import Personaldata


@dp.callback_query_handler(state=Personaldata.Selections.lan, text=["uz", "ru"])
async def done_language(call: types.CallbackQuery, state: FSMContext):
    await db.update_language_db(language_db=call.data, telegram_id=call.message.chat.id)
    await call.message.delete()
    await state.finish()
    language_request_welcome_2 = await db.select_users_one(telegram_id=call.message.chat.id)
    await call.message.answer(text=welcome[language_request_welcome_2['language_db']])
    await orientation_lan(user_id=call.message.chat.id, locale=language_request_welcome_2['language_db'])
    await Personaldata.Welcome.wel.set()


@dp.callback_query_handler(text=["uz", "ru"])
async def done_language(call: types.CallbackQuery):
    if call.data == "uz":
        await call.message.answer("<b>Sozlama o'rnatildi!</b>")
    elif call.data == "ru":
        await call.message.answer("<b>Настройка установлена!</b>")
    await db.update_language_db(language_db=call.data, telegram_id=call.message.chat.id)
    await call.message.delete()


@dp.message_handler(commands=['til'])
async def start(message: types.Message):
    await send_start_lan(user_id=message.from_user.id)
