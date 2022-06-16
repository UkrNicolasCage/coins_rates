from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter
from tgbot.misc.refresh_rates import refresh_data
admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["start"], state="*")
async def admin_start(message: Message,  state: FSMContext):
    
    await state.set_state('usd') 
    await message.reply(f"Good morning, Master!")
    

    
    
@admin_router.message(commands=["refresh"], state="*")
async def refr_rates(message: Message):
    await message.answer(text="start refreshing...")
        
    await refresh_data()
    
    await message.answer(text="refreshing is complete")
