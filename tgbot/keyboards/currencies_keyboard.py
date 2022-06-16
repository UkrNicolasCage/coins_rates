from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



currency_keyboard = InlineKeyboardBuilder()


currency_keyboard.row(InlineKeyboardButton(
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
