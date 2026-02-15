import logging
import sys
from pathlib import Path
from typing import Optional


class LoggerSetup:

    @staticmethod
    def setup(log_dir: str, app_name: str = "watchtower-bot") -> logging.Logger:
        Path(log_dir).mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(app_name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            file_handler = logging.FileHandler(f"{log_dir}/bot.log")
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(console_handler)

        return logger