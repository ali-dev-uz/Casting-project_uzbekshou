from aiogram import types
from aiogram.dispatcher import FSMContext
from handlers.users.archive import ADMIN_S, CHANNELS
from keyboards.default.menuKeyboard import menu_admin, back
from loader import dp
from states import Personaldata


# Orqaga qaytish
@dp.message_handler(state=Personaldata.Organ.chan, text="🔙 Orqaga")
async def back_key_organ(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_S:
        await message.answer("Bosh menyu", reply_markup=menu_admin)
        await state.finish()


@dp.message_handler(text="📢 Kanal sozlash")
async def add_group(message: types.Message):
    if message.from_user.id in ADMIN_S:
        msg = "<b>Yangi kanal qo'shish yoki o'chirish uchun\n" \
              "shu kanalning ID raqamini yoki Ijtimoiy tarmoq Havola manzilini  yuboring.</b>\n" \
              "(Namuna: -1003432134 or https://....)\n\n" \
              "<b>Ulangan kanalar:</b>\n"
        a = 1
        for mavjud in CHANNELS:
            try:
                if str(mavjud[:6]) == "https:":
                    msg += f"{a})Havola:<i>{mavjud}</i>\n"
            except:
                try:
                    info = await dp.bot.get_chat(chat_id=mavjud)
                    msg += f"{a})ID:<i>{mavjud} -- {info.full_name}\n{info.invite_link}</i>\n"
                except:
                    msg += f"{a})ID:<i>{mavjud}</i>\n"

            a += 1
        await message.answer(text=msg,
                             reply_markup=back)
        await Personaldata.Organ.chan.set()


@dp.message_handler(state=Personaldata.Organ.chan, content_types=types.ContentType.TEXT)
async def delete_channel(message: types.Message, state: FSMContext):
    try:
        try:
            url = str(message.text[:6])
            if url == 'https:':
                if message.text in CHANNELS:
                    CHANNELS.remove(message.text)
                    await message.answer("🔴 Havola o'chirildi", reply_markup=menu_admin)
                    await state.finish()
                else:
                    CHANNELS.append(message.text)
                    await message.answer("🟢 Havola qo'shildi", reply_markup=menu_admin)
                    await state.finish()
            else:
                kodd = int(message.text)
                try:
                    status = await dp.bot.get_chat_administrators(chat_id=kodd)
                    if kodd in CHANNELS:
                        CHANNELS.remove(kodd)
                        await message.answer("🔴 Kanal o'chirildi", reply_markup=menu_admin)
                        await state.finish()
                    else:
                        CHANNELS.append(kodd)
                        await message.answer("🟢 Kanal qo'shildi", reply_markup=menu_admin)
                        await state.finish()
                except:
                    if message.forward_from_chat.id in CHANNELS:
                        CHANNELS.remove(kodd)
                        await message.answer("🔴 Kanal o'chirildi", reply_markup=menu_admin)
                        await state.finish()
                    else:
                        await message.answer(
                            "<b>Uzr, Bot ushbu kanalning adminlar ruyxatida mavjud emas, Bot ushbu kanalga ADMIN bo'lmaguncha 'Kanalar' ruyxatiga kiritilmaydi!</b>")

        except:
            kodd = int(message.text)
            try:
                status = await dp.bot.get_chat_administrators(chat_id=kodd)
                if kodd in CHANNELS:
                    CHANNELS.remove(kodd)
                    await message.answer("🔴 Kanal o'chirildi", reply_markup=menu_admin)
                    await state.finish()
                else:
                    CHANNELS.append(kodd)
                    await message.answer("🟢 Kanal qo'shildi", reply_markup=menu_admin)
                    await state.finish()
            except:
                if message.forward_from_chat.id in CHANNELS:
                    CHANNELS.remove(kodd)
                    await message.answer("🔴 Kanal o'chirildi", reply_markup=menu_admin)
                    await state.finish()
                else:
                    await message.answer(
                        "<b>Uzr, Bot ushbu kanalning adminlar ruyxatida mavjud emas, Bot ushbu kanalga ADMIN bo'lmaguncha 'Kanalar' ruyxatiga kiritilmaydi!</b>")

    except:
        await message.answer("Iltimos faqat ID yoki Havola yuboring!")
