from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.get_list_of_coins import get_coins_names_list

class IsReal(BaseFilter): # клас для фільтрування повідомлень з криптовалютами
    async def __call__(self, obj: Message) -> bool: # метод для перевірки чи повідомлення є назвою криптовалюти
        return (obj.text.lower() in get_coins_names_list(lower_case= True)) == True 
