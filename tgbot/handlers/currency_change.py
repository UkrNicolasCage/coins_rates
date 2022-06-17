from aiogram import F, Router
from aiogram.types import Message,CallbackQuery
from aiogram.dispatcher.fsm.context import FSMContext


from tgbot.keyboards.currencies_keyboard import currency_keyboard

currency_router = Router()


@currency_router.message(commands=["change_currency"])
async def show_change_currency_menu(message: Message):
    await message.answer(
        text="Please, select the currency you want to change",
        reply_markup=currency_keyboard.as_markup())
    
    
    
@currency_router.callback_query(text="usd")
@currency_router.callback_query(text="uah")
@currency_router.callback_query(text="eur")
async def change_currency(call: CallbackQuery, state: FSMContext):
    call.message.delete_reply_markup()
    choiced_cuurrency = call.data
    if choiced_cuurrency == "usd":
        await state.set_state('usd')
        await call.message.answer(text=f"Currency changed to dollar")
    elif choiced_cuurrency == "uah":
        await state.set_state('uah')
        await call.message.answer(text=f"Currency changed to hrivna")
    elif choiced_cuurrency == "eur":
        await state.set_state('eur')
        await call.message.answer(text=f"Currency changed to euro")
    else:
        await call.message.answer(text=f"Something went wrong")
        
    
