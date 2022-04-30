from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message
import json 
from tgbot.config import Config
from tgbot.misc.get_list_of_coins import get_coins_names_list


class IsReal(BaseFilter):
    is_real: bool = True
    

    async def __call__(self, obj: Message, config: Config) -> bool:
        return (obj.text in get_coins_names_list()) == self.is_real
