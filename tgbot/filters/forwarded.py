from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message



class ForwardedMessageFilter(BaseFilter):
    
    async def __call__(self, obj: Message) -> bool:
        return obj.forward_from == None