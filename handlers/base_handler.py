from telegram import Update
from telegram.ext import ContextTypes
from core.exceptions import UnauthorizedError
from typing import Callable, Coroutine, Any
import functools


class BaseHandler:

    def __init__(self, authorized_chat_ids: list[int]):
        self.authorized_chat_ids = authorized_chat_ids

    def auth_required(self, handler_func: Callable) -> Callable:
        @functools.wraps(handler_func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
            if not update.effective_chat or update.effective_chat.id not in self.authorized_chat_ids:
                raise UnauthorizedError(f"Unauthorized access from {update.effective_chat.id}")
            return await handler_func(self, update, context)

        return wrapper