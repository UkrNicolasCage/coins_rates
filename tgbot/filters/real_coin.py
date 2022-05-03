from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from tgbot.misc.get_list_of_coins import get_coins_names_list

class IsReal(BaseFilter):
    async def __call__(self, obj: Message) -> bool:
        return (obj.text.lower() in get_coins_names_list(lower_case= True)) == True
