from telegram import Update
from telegram.ext import ContextTypes
from repositories.log_repository import LogRepository
from .base_handler import BaseHandler
from core.security import SecurityService


class LogsHandler(BaseHandler):

    def __init__(self, authorized_chat_ids: list[int], log_repository: LogRepository):
        super().__init__(authorized_chat_ids)
        self.log_repository = log_repository

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.check_authorization(update)

        logs = self.log_repository.get_recent_logs(limit=5)

        if not logs:
            await update.message.reply_text("There are no saved update logs")
            return

        text = "Last update logs:\n"
        for i, (filename, size, timestamp) in enumerate(logs, 1):
            safe_filename = SecurityService.escape_markdown_v2(filename)
            text += f"{i}. `{safe_filename}` ({size} byte, {timestamp})\n"

        await update.message.reply_text(text)