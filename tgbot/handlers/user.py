import json
from aiogram import F, Router
from aiogram.types import Message,CallbackQuery

from tgbot.filters.real_coin import IsReal
from tgbot.keyboards.common_keyboard import common_coins_keyboard
user_router = Router()



@user_router.message(commands=["start"])
@user_router.message(commands=["help"])
async def user_start(message: Message):
    await message.answer("Enter the desired cryptocurrency.\n"
                        "Examples: 'btc', 'Bitcoin'\n\n"
                        "Or just click on /common and get the most common cryptocurrencies")


 
@user_router.message(F.text, IsReal(), state="*")
async def get_coin_info(message: Message):
    with open("tgbot\\models\\exchange_rates.json","r", encoding="utf-8") as file:
        coins = json.load(file)
        for coin in coins:
            if coin.get('name_long') == message.text or coin.get("name_short") == message.text:
                name_long = coin.get("name_long")
                name_short = coin.get("name_short")
                price = coin.get("price")
                capitalized = coin.get("capitalized")
                days_change = coin.get("days_change")
                if days_change[0] == "-":
                    days_change = days_change + "%📉"
                else:
                    days_change = days_change + "%📈"
                break                
                
    await message.answer(text = f"{name_long}({name_short})\n"
                        f"Price:  {price} USD\n"
                        f"days_change:  {days_change}\n"
                        f"capitalized:  {capitalized} USD")
            
                    
@user_router.message(commands=["there"])
@user_router.message(commands=["common"])
async def get_common(message: Message):
    await message.answer(text = "click on desired cryptocurrency⬇️",
                         reply_markup=common_coins_keyboard.as_markup())          
                     

@user_router.message(F.text, state="*")
async def no_coin(message: Message):
            await message.answer("We haven't it. Please check the spelling of cryptocurrency and retype it.\n"
                                 "Also you can get the most common cryptocurrencies /there")
            
                 
@user_router.callback_query(state="*")
async def find_common_keyboard(call: CallbackQuery):
    with open("tgbot\\models\\exchange_rates.json","r", encoding="utf-8") as file:
        coins = json.load(file)
        for coin in coins:
            if coin.get("name_short") == call.data:
                name_long = coin.get("name_long")
                name_short = coin.get("name_short")
                price = coin.get("price")
                capitalized = coin.get("capitalized")
                days_change = coin.get("days_change")
                if days_change[0] == "-":
                    days_change = days_change + "%📉"
                else:
                    days_change = days_change + "%📈"
                break                
                
    await call.message.answer(text = f"{name_long}({name_short})\n"
                        f"Price:  {price} USD\n"
                        f"days_change:  {days_change}\n"
                        f"capitalized:  {capitalized} USD")
    await call.answer()
