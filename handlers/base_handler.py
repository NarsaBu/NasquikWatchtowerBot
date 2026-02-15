from telegram import Update
from core.exceptions import UnauthorizedError


class BaseHandler:

    def __init__(self, authorized_chat_ids: list[int]):
        self.authorized_chat_ids = authorized_chat_ids

    async def check_authorization(self, update: Update) -> None:
        if not update.effective_chat:
            raise UnauthorizedError("Unknown chat")
        if update.effective_chat.id not in self.authorized_chat_ids:
            await update.message.reply_text(
                f"Access denied\\. Your \\chat_id: `{update.effective_chat.id}`",
                parse_mode='MarkdownV2'
            )
            raise UnauthorizedError(f"Unauthorized access from chat_id {update.effective_chat.id}")