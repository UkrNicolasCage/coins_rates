from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



currency_keyboard = InlineKeyboardBuilder() # клас для створення клавіатури


currency_keyboard.row(InlineKeyboardButton( # заповнення клавіатури 
        text="Hrivna",      
        callback_data="uah" 
    ),      
    InlineKeyboardButton( 
        text="Dollar",
        callback_data="usd",
    ),
    InlineKeyboardButton(
        text="Euro",
        callback_data="eur",
    )
    )
