import json
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.misc.read_request_history import get_request_history_info



def recent_keyboard(id):
    recent = InlineKeyboardBuilder()
    users = get_request_history_info()
    for user in users:
        if user.get("id") == id:
            history = user.get("history")
            
    for coin in history:
        recent.row(InlineKeyboardButton(text=coin, callback_data=coin ))
        
    return recent.as_markup()
    
        