from aiogram import types
from aiogram.dispatcher import FSMContext

from filters import IsGroup
from handlers.users.archive import ADMIN_S
from keyboards.default.menuKeyboard import back, menu_admin
from loader import dp
from states import Personaldata


# Bu faqat adminlar buyruqlari
@dp.message_handler(state=Personaldata.Manual.manual_done, text="🔙 Orqaga")
async def back_key(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_S:
        await message.answer("Bosh menyu", reply_markup=menu_admin)
        await state.finish()


@dp.message_handler(IsGroup(), text="👨🏻‍💻 Admin qo'shish")
async def add_admin(message: types.Message):
    if message.from_user.id in ADMIN_S:
        await message.answer("Yangi admin qo'shish yoki o'chirish uchun Telegram ID raqamini yuboring !",
                             reply_markup=back)
        await Personaldata.Manual.manual_done.set()


@dp.message_handler(state=Personaldata.Manual.manual_done, content_types=types.ContentType.TEXT)
async def delete_admin(message: types.Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        if admin_id in ADMIN_S:
            ADMIN_S.remove(admin_id)
            await state.finish()
            await message.answer("🔴 Adminlikdan olib tashlandi !", reply_markup=menu_admin)
        else:
            ADMIN_S.append(admin_id)
            await state.finish()
            await message.answer("🟢 Admin qilindi !", reply_markup=menu_admin)
    except:
        await message.answer("ID noto'g'ri, iltimos qayta yuboring")
