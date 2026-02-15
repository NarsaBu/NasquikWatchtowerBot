from telegram import Update
from telegram.ext import ContextTypes
from core.security import SecurityService
from .base_handler import BaseHandler


class StartHandler(BaseHandler):
    def __init__(self, authorized_chat_ids: list[int], allowed_scopes: list[str]):
        super().__init__(authorized_chat_ids)
        self.allowed_scopes = allowed_scopes

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.check_authorization(update)

        help_text = (
                "🛡️ *Watchtower Control Bot*\n\n"
                "Available commands:\n"
                "• `/update <scope>` — update services in scopes\n"
                "• `/check <scope>` — check scope for update \\(without applying\\)\n"
                "• `/scopes` — list of available scopes\n"
                "• `/logs` — list last 5 log files\n"
                "• `/help` — list of available commands\n\n"
                "Available scopes: " + ", ".join([f"`{s}`" for s in self.allowed_scopes])
        )
        await update.message.reply_text(help_text, parse_mode='MarkdownV2')