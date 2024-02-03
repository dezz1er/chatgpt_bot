from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from db.user import User


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            user_id = (event.message.from_user.id
                       if event.event_type == "message"
                       else event.callback_query.from_user.id)
            data["user"] = await session.scalar(
                select(User).where(User.user_id == user_id)
            )

            return await handler(event, data)
