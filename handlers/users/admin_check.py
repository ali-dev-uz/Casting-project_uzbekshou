import ast
import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import exceptions

from handlers.users.vocabulary_words import not_response, pay_data_1, done_response, pay_data_2, \
    pay_data_3, pay_data_4, pay_button
from loader import dp, db
from utils.counter_payme import fetch_data


@dp.callback_query_handler(text=['not', 'done', 'tips'])
async def admin_check_handler(call: types.CallbackQuery):
    message_id = call.message.message_id
    data_all = await db.select_message_data(message_id)
    casting_user = data_all['telegram_id']
    language_request_caster = await db.select_users_one(telegram_id=casting_user)
    try:
        if call.data == 'not':
            await dp.bot.send_message(chat_id=casting_user, text=not_response[language_request_caster['language_db']])
        elif call.data == 'done':
            usd = await fetch_data()
            pay_counter = usd * 80
            inline_keyboard_admin = InlineKeyboardMarkup(row_width=1)
            inline_admin = InlineKeyboardButton(f"{pay_button[language_request_caster['language_db']]}",
                                                callback_data="pay")
            inline_keyboard_admin.add(inline_admin)
            await dp.bot.send_message(chat_id=casting_user,
                                      text=f"{done_response[language_request_caster['language_db']]}\n"
                                           f"{pay_data_1[language_request_caster['language_db']]}\n"
                                           f"{pay_data_2[language_request_caster['language_db']]} 80$ (🇺🇿{pay_counter}{pay_data_3[language_request_caster['language_db']]})\n"
                                           f"{pay_data_4[language_request_caster['language_db']]}",
                                      reply_markup=inline_keyboard_admin)
        elif call.data == "tips":
            usd = await fetch_data()
            pay_counter = usd * 40
            inline_keyboard_admin = InlineKeyboardMarkup(row_width=1)
            inline_admin = InlineKeyboardButton(f"{pay_button[language_request_caster['language_db']]}",
                                                callback_data="pay")
            inline_keyboard_admin.add(inline_admin)
            try:
                await dp.bot.send_message(chat_id=casting_user,
                                          text=f"{done_response[language_request_caster['language_db']]}\n"
                                               f"{pay_data_1[language_request_caster['language_db']]}\n"
                                               f"{pay_data_2[language_request_caster['language_db']]} 40$ (🇺🇿{pay_counter}{pay_data_3[language_request_caster['language_db']]})\n"
                                               f"{pay_data_4[language_request_caster['language_db']]}",
                                          reply_markup=inline_keyboard_admin)
            except exceptions.ChatNotFound as e:
                logging.error(f"ChatNotFound error: {e}")


        for delete_data in await db.select_all_data(casting_user):
            try:
                string_list_loop = delete_data["photo_id"]
                result_list_loop = ast.literal_eval(string_list_loop)
                for loop_id in result_list_loop:
                    await dp.bot.delete_message(chat_id=delete_data['chat_id'],
                                                message_id=loop_id)
                await dp.bot.delete_message(chat_id=delete_data['chat_id'],
                                            message_id=delete_data['message_id'])
            except exceptions.ChatNotFound as e:
                logging.error(f"ChatNotFound error: {e}")
        await db.delete_data(casting_user)
    except exceptions.ChatNotFound as e:
        logging.error(f"ChatNotFound error: {e}")

