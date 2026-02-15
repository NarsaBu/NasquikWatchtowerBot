from telegram import Bot
from telegram.error import TelegramError
import asyncio
from core.security import SecurityService


class TelegramService:

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_chunked(
            self,
            chat_id: int,
            text: str,
            parse_mode: str = 'MarkdownV2',
            max_retries: int = 3
    ) -> None:
        safe_text = SecurityService.escape_markdown_v2(text)

        for attempt in range(max_retries):
            try:
                chunks = [safe_text[i:i + 4000] for i in range(0, len(safe_text), 4000)] # Telegram limit 4096 symbols
                for chunk in chunks:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=chunk,
                        parse_mode=parse_mode
                    )
                    await asyncio.sleep(0.1)  # rate-limit
                return
            except TelegramError as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(2 ** attempt)  # exponential delay