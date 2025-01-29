from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject, Message
from typing import Callable, Dict, Any, Awaitable

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage


    async def __call__(self,
                       handler: Callable[[TelegramObject,Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ):
        user = event.from_user
        user_name = user.username
        check_user = await self.storage.redis.get(name=user_name)


        if check_user:
            if int(check_user.decode())==1:
                await self.storage.redis.set(name=user_name, value=0,ex=10)
                return await event.answer("Ждите 10 сек")
            return
        await self.storage.redis.set(name=user_name, value=1,ex=10)

        return await handler(event, data)