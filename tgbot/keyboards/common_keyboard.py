from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



common_coins_keyboard = InlineKeyboardBuilder()

common_coins_keyboard.row(InlineKeyboardButton(
        text="Bitcoin",
        callback_data="btc"
    ),
    InlineKeyboardButton(
        text="Solana",
        callback_data="sol",
    ),
    InlineKeyboardButton(
        text="Cardano",
        callback_data="ada",
    )
    )

common_coins_keyboard.row(InlineKeyboardButton(
        text="Avalanche",
        callback_data="avax"
    ),
    InlineKeyboardButton(
        text="Dogecoin",
        callback_data="doge",
    ),
    InlineKeyboardButton(
        text="Polkadot",
        callback_data="dot",
    )
    )