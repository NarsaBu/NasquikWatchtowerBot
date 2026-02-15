from telegram import Update
from telegram.ext import ContextTypes
from core.security import SecurityService
from .base_handler import BaseHandler


class ScopesHandler(BaseHandler):

    def __init__(self, authorized_chat_ids: list[int], allowed_scopes: list[str]):
        super().__init__(authorized_chat_ids)
        self.allowed_scopes = allowed_scopes

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.check_authorization(update)

        if not self.allowed_scopes:
            await update.message.reply_text("There are no allowed scopes for update")
            return

        text = "Allowed scopes for update:\n"
        for scope in sorted(self.allowed_scopes):
            text += f"• `{scope}`\n"

        await update.message.reply_text(text)