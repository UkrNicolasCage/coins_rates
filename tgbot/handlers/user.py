import json
from aiogram import F, Bot, Router
from aiogram.types import Message,CallbackQuery, FSInputFile
from tgbot.config import  load_config

from tgbot.filters.real_coin import IsReal
from tgbot.filters.forwarded import ForwardedMessageFilter
from tgbot.keyboards.common_keyboard import common_coins_keyboard
from tgbot.keyboards.recent import recent_keyboard
from tgbot.misc.change_history import change
from tgbot.misc.read_request_history import get_request_history_info 
user_router = Router()


@user_router.message(ForwardedMessageFilter(),commands=["start"])
async def user_start(message: Message ):
    flag = False
    users = get_request_history_info()
    
    if users:
        for user in users:
            if message.from_user.id  == user.get("id"):
                flag = True
                    
    if flag == False:
        users.append({ "id": message.from_user.id,"history": []})            
        
        with open("tgbot/models/request_history.json", "w") as file :   
            json.dump(users, file, indent=4, ensure_ascii=False)
            
    await message.answer("Enter the desired cryptocurrency.\n"
                        "Examples: 'btc', 'Bitcoin'\n\n"
                        "Or just click on /common and get the most common cryptocurrencies")        

 
@user_router.message(commands=["start"])
async def user_start(message: Message ):
    await message.answer("Please do not forward messages. We only accept original messages.")
        
        
@user_router.message(commands=["help"])
async def user_start(message: Message ):
    await message.answer("Enter the desired cryptocurrency.\n"
                        "Examples: 'btc', 'Bitcoin'\n\n"
                        "or just click on /common and get the most common cryptocurrencies.\n"
                        "Also you can get your recent requests on /recently")
    


@user_router.message(commands=["recently"])
async def get_recently_requests(message: Message):
    await message.answer(text="Your recent requests⏱", reply_markup=recent_keyboard(message.from_user.id))  
    
@user_router.message(commands=["get_in_file"]) 
async def get_files(message: Message):
    config = load_config(".env")
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    await bot.send_document(chat_id= message.from_user.id, 
                        document = FSInputFile(path= "tgbot/models/exchange_rates.json")
                        )
       

       
       
@user_router.message(F.text, IsReal(), state="*")
async def get_coin_info(message: Message):
    with open("tgbot/models/exchange_rates.json","r", encoding="utf-8") as file:
        coins = json.load(file)
        for coin in coins:
            if coin.get('name_long').lower() == message.text.lower() or coin.get("name_short").lower() == message.text.lower():
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
    users = get_request_history_info()               
    with open("tgbot/models/request_history.json", "w") as file :   
        
        for user in users:
            if user.get("id") == message.from_user.id:
                user["history"] = change(user.get("history"), message.text)
            
        json.dump(users, file, indent=4, ensure_ascii=False)
        
    await message.answer(text = f"{name_long}({name_short})\n"
                        f"Price:  {price} USD\n"
                        f"days_change:  {days_change}\n"
                        f"capitalized:  {capitalized} USD")
            
                    
@user_router.message(commands=["there"])
@user_router.message(commands=["common"])
async def get_common(message: Message):
    await message.answer(text = "Click on desired cryptocurrency⬇️",
                         reply_markup=common_coins_keyboard.as_markup())          
                     

@user_router.message(F.text, state="*")
async def no_coin(message: Message):
            await message.answer("We haven't it. Please check the spelling of cryptocurrency and retype it.\n"
                                 "Also you can get the most common cryptocurrencies /there")
            
                 
@user_router.callback_query(state="*")
async def find_common_keyboard(call: CallbackQuery):
    with open("tgbot/models/exchange_rates.json","r", encoding="utf-8") as file:
        coins = json.load(file)
        for coin in coins:
            if coin.get("name_short") == call.data or coin.get("name_long") == call.data:
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
                      
    users = get_request_history_info()               
    with open("tgbot/models/request_history.json", "w") as file :   
        
        for user in users:
            if user.get("id") == call.from_user.id:
                user["history"] = change(user.get("history"), call.data)
            
        json.dump(users, file, indent=4, ensure_ascii=False)
        
        
    await call.message.answer(text = f"{name_long}({name_short})\n"
                        f"Price:  {price} USD\n"
                        f"days_change:  {days_change}\n"
                        f"capitalized:  {capitalized} USD")
    await call.answer()


