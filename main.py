import asyncio
import sys
from telegram.ext import Application, CommandHandler
from config import BotConfig
from core.logger import LoggerSetup
from core.exceptions import WatchtowerBotError
from services.docker_service import DockerService
from services.telegram_service import TelegramService
from repositories.log_repository import LogRepository
from handlers.start_handler import StartHandler
from handlers.update_handler import UpdateHandler
from handlers.check_handler import CheckHandler
from handlers.scopes_handler import ScopesHandler
from handlers.logs_handler import LogsHandler


async def main() -> None:
    try:
        config = BotConfig.from_env()
        config.validate()
    except ValueError as e:
        print(f"❌ Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)

    logger = LoggerSetup.setup(config.log_dir)
    logger.info("Запуск Watchtower Telegram Bot")

    docker_service = DockerService(config.docker_sock, config.watchtower_image)
    log_repository = LogRepository(config.log_dir)

    application = Application.builder().token(config.telegram_token).build()
    telegram_service = TelegramService(application.bot)

    start_handler = StartHandler(config.authorized_chat_ids, config.allowed_scopes)
    update_handler = UpdateHandler(
        config.authorized_chat_ids,
        docker_service,
        telegram_service,
        log_repository,
        config.allowed_scopes
    )
    check_handler = CheckHandler(
        config.authorized_chat_ids,
        docker_service,
        telegram_service,
        log_repository,
        config.allowed_scopes
    )
    scopes_handler = ScopesHandler(config.authorized_chat_ids, config.allowed_scopes)
    logs_handler = LogsHandler(config.authorized_chat_ids, log_repository)

    application.add_handler(CommandHandler("start", start_handler.handle))
    application.add_handler(CommandHandler("update", update_handler.handle))
    application.add_handler(CommandHandler("check", check_handler.handle))
    application.add_handler(CommandHandler("scopes", scopes_handler.handle))
    application.add_handler(CommandHandler("logs", logs_handler.handle))
    application.add_handler(CommandHandler("help", start_handler.handle))

    logger.info(f"Bot has been started. Authorized chat_ids: {config.authorized_chat_ids}")
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

    logger.info("Bot is ready for use.")
    stop_event = asyncio.Event()
    await stop_event.wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot has been stopped by user.")
    except WatchtowerBotError as e:
        print(f"Bot exception: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Bot unexpected exception: {e}", file=sys.stderr)
        sys.exit(1)