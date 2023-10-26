from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.users.start import orientation_lan, send_start_lan
from handlers.users.vocabulary_words import welcome, types_direction, casting_text, species_keyword
from loader import dp, db
from states import Personaldata


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



