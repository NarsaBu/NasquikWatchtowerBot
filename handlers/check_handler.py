from telegram import Update
from telegram.ext import ContextTypes
from services.docker_service import DockerService
from services.telegram_service import TelegramService
from repositories.log_repository import LogRepository
from core.security import SecurityService
from .base_handler import BaseHandler
import asyncio
from pathlib import Path


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
            await update.message.reply_text("Select scope: `/check qbittorrent`", parse_mode='MarkdownV2')
            return

        scope = context.args[0].lower()
        if not SecurityService.validate_scope(scope, self.allowed_scopes):
            scopes_list = ", ".join([f"`{s}`" for s in self.allowed_scopes])
            await update.message.reply_text(
                f"Unavailable scope `{scope}`\nAvailable scopes: {scopes_list}",
                parse_mode='MarkdownV2'
            )
            return

        await update.message.reply_text(f"Starting check for the scope `{scope}`...", parse_mode='MarkdownV2')

        log_path = await self.log_repository.create_log_file(scope, is_check=True)
        chat_id = update.effective_chat.id

        try:
            summary_lines = []
            last_sent = 0

            async for line in self.docker_service.run_watchtower(scope, is_check=True):
                await self.log_repository.save_line(log_path, line)
                summary_lines.append(line)

                if (len(summary_lines) - last_sent >= 15) or any(
                        kw in line.lower() for kw in ['pulling', 'checking', 'found', 'error', 'failed']
                ):
                    preview = '\n'.join(summary_lines[-10:])
                    await self.telegram_service.send_chunked(
                        chat_id,
                        f"Checking scope `{scope}`:\n```\n{preview}\n```"
                    )
                    last_sent = len(summary_lines)

            # Финальный отчёт
            summary = '\n'.join(summary_lines[-30:])
            await self.telegram_service.send_chunked(
                chat_id,
                f"Check for the scope `{scope}` has been finished\\.\n"
                f"Лог: `{Path(log_path).name}`\n\n"
                f"```\n{summary[-3000:]}\n```"
            )

        except Exception as e:
            error_msg = str(e)
            await self.telegram_service.send_chunked(
                chat_id,
                f"Error while checking the scope `{scope}`:\n```\n{error_msg}\n```"
            )