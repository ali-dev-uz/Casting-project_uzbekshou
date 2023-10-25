from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_admin = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='📊 Statistika'),  # menu bulimiga knopka quyish
            KeyboardButton(text='🎞 Kino yuklash'),  # menu bulimiga knopka quyish

        ],
        [
            KeyboardButton(text='📢 Kanal sozlash'),  # menu bulimiga knopka quyish
            KeyboardButton(text="👨🏻‍💻 Admin qo'shish"),  # menu bulimiga knopka quyish

        ],
        [
            KeyboardButton(text='📧 Reklama yuborish'),  # menu bulimiga knopka quyish
        ]
    ],
    resize_keyboard=True
)



back = ReplyKeyboardMarkup(
    keyboard=[

        [
            KeyboardButton(text='🔙 Orqaga'),  # menu bulimiga knopka quyish

        ]


    ],
    resize_keyboard=True

)
