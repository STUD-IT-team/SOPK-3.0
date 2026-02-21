from dependency_injector.wiring import inject, Provide
from injection import Container
from typing import Any, Dict
import logging

from aiogram.types import Update, Message

__all__ = ["LogMiddleware"]

@inject
class LogMiddleware:
    logger: logging.Logger = Provide[Container.logger]

    async def __call__(
        self,
        handler: callable,
        event: Update,
        data: Dict[str, Any],
    ):
        self.logger.info(f"Got new update from {event.message.chat.id}:{event.message.chat.username}. Text: {event.message.text}")
        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.error(f"Error in handler for {event.message.chat.id}:{event.message.chat.username}. Text: {event.message.text}. Error: {e}")
        self.logger.info(f"Finished handling {event.message.chat.id}:{event.message.chat.username}. Text: {event.message.text}")
        return
