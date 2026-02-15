from telegram import Update
from telegram.ext import ContextTypes
from services.docker_service import DockerService
from services.telegram_service import TelegramService
from repositories.log_repository import LogRepository
from core.security import SecurityService
from .base_handler import BaseHandler
import asyncio
from pathlib import Path
from datetime import datetime


class CheckHandler(BaseHandler):

    def __init__(
            self,
            authorized_chat_ids: list[int],
            docker_service: DockerService,
            telegram_service: TelegramService,
            log_repository: LogRepository,
            allowed_scopes: list[str]
    ):
        super().__init__(authorized_chat_ids)
        self.docker_service = docker_service
        self.telegram_service = telegram_service
        self.log_repository = log_repository
        self.allowed_scopes = allowed_scopes

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await self.check_authorization(update)

        if not context.args:
            await update.message.reply_text("Select scope: `/check qbittorrent`")
            return

        scope = context.args[0].lower()
        if not SecurityService.validate_scope(scope, self.allowed_scopes):
            scopes_list = ", ".join(self.allowed_scopes)
            await update.message.reply_text(
                f"Unavailable scope `{scope}`\nAvailable scopes: {scopes_list}"
            )
            return

        msg = await update.message.reply_text(f"Starting check for the scope `{scope}`...")

        log_path = await self.log_repository.create_log_file(scope, is_check=True)
        log_filename = Path(log_path).name

        try:
            success, summary, _ = await self.docker_service.run_watchtower(
                scope=scope,
                log_path=log_path,
                is_check=True
            )

            status_emoji = "✅" if success else "❌"
            await msg.edit_text(
                f"{status_emoji} Check '{scope}' is completed:\n"
                f"{summary}\n\n"
                f"Log: {log_filename}"
            )

        except Exception as e:
            error_msg = str(e)[:500]  # обрезать длинные ошибки
            await msg.edit_text(
                f"Error while checking the scope '{scope}':\n{error_msg}\n\n"
                f"Log: {log_filename}"
            )