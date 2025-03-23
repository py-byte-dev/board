from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from dishka import AsyncContainer

from backend.config import Config


class UserAcessMiddleware(BaseMiddleware):
    def __init__(
        self,
        container: AsyncContainer,
    ) -> None:
        self._container = container

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        async with self._container() as container:
            config = await container.get(Config)

        if event.from_user.id in config.bot.admins:
            return await handler(event, data)
