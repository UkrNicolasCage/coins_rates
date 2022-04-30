from aiogram import Router
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter
from tgbot.misc.refresh_rates import refresh_data

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["start"], state="*")
async def admin_start(message: Message):
    await message.reply("Good morning, Master!")


@admin_router.message(commands=["refresh"], state="*")
async def refr_rates(message: Message):
    await message.answer(text="start refreshing...")
        
    await refresh_data()
    
    await message.answer(text="refreshing is complete")
