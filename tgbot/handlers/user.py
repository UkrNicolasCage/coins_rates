import json
from locale import currency
from aiogram import F, Bot, Router
from aiogram.types import Message,CallbackQuery, FSInputFile
from aiogram.dispatcher.fsm.context import FSMContext
from tgbot.config import  load_config

from tgbot.filters.real_coin import IsReal
from tgbot.filters.forwarded import ForwardedMessageFilter
from tgbot.keyboards.common_keyboard import common_coins_keyboard
from tgbot.keyboards.recent import recent_keyboard
from tgbot.misc.change_history import change
from tgbot.misc.create_answer import create_answer
from tgbot.misc.read_request_history import get_request_history_info 



user_router = Router()

@user_router.message(ForwardedMessageFilter(),commands=["start"])
async def user_start(message: Message, state: FSMContext ):
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
    await state.set_state('usd')       
    await message.answer("Enter the desired cryptocurrency.\n"
                        "Examples: 'btc', 'Bitcoin'\n\n"
                        "Or just click on /common and get the most common cryptocurrencies"
                        "also you can chanege currency of price on /change_currency,") 
 

 
@user_router.message(commands=["start"])
async def user_start(message: Message):
    await message.answer("Please do not forward messages. We only accept original messages.")
    
        
@user_router.message(commands=["help"])
async def user_start(message: Message,  ):
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
                            document = FSInputFile(
                                path= "tgbot/models/exchange_rates_usd.json")
                            )
    await bot.send_document(chat_id=message.from_user.id,
                            document=FSInputFile(
                                path="tgbot/models/exchange_rates_eur.json")
                            )
    await bot.send_document(chat_id=message.from_user.id,
                            document=FSInputFile(
                                path="tgbot/models/exchange_rates_uah.json")
                            )
       

       
@user_router.message(F.text, IsReal(),state='usd')
@user_router.message(F.text, IsReal(), state='eur')
@user_router.message(F.text, IsReal(), state='uah')
async def get_coin_info(message: Message, state: FSMContext):
    currency = str(await state.get_state())
    answer = await create_answer(id=message.from_user.id, data=message.text, currency=currency)

    await message.answer(text=answer)
            
                    
@user_router.message(commands=["there"])
@user_router.message(commands=["common"])
async def get_common(message: Message):
    await message.answer(text = "Click on desired cryptocurrency⬇️",
                         reply_markup=common_coins_keyboard.as_markup())          
                     

@user_router.message(F.text, state="*")
async def no_coin(message: Message):
            await message.answer("We haven't it. Please check the spelling of cryptocurrency and retype it.\n"
                                 "Also you can get the most common cryptocurrencies /there")
            
@user_router.callback_query(state='usd')
@user_router.callback_query(state='eur')             
@user_router.callback_query(state='uah')
async def find_common_keyboard(call: CallbackQuery, state: FSMContext):
    currency = str(await state.get_state())
    answer = await create_answer(id = call.from_user.id,data = call.data, currency = currency)
    call.answer()
    await call.message.answer(text = answer)
    


