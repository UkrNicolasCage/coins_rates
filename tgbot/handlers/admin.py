from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher.fsm.context import FSMContext

from tgbot.filters.admin import AdminFilter
from tgbot.misc.refresh_rates import refresh_data
admin_router = Router() # створення роутера, до якого буде прив'язано всі хендлери з файлу admin.py
admin_router.message.filter(AdminFilter()) # додається фільтр для адміністратора


@admin_router.message(commands=["start"], state="*")
async def admin_start(message: Message,  state: FSMContext):
    
    await state.set_state('usd') 
    await message.reply(f"Good morning, Master!")
    

    
    
@admin_router.message(commands=["refresh"], state="*") # прив'язується хендлер до роутера
async def refr_rates(message: Message): 
    await message.answer(text="start refreshing...") # повідомляєьться користувача про початок оновлення

    await refresh_data() # виконується оновлення даних
    
    await message.answer(text="refreshing is complete") # повідомлюємо користувача про завершення оновлення
