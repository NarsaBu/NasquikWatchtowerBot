import os
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class BotConfig(BaseModel):
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")
    authorized_chat_ids: List[int] = Field(default_factory=list)
    allowed_scopes: List[str] = Field(default_factory=list)
    log_dir: str = "/app/logs"
    watchtower_image: str = "containrrr/watchtower:latest"
    docker_sock: str = "/var/run/docker.sock"

    class Config:
        validate_assignment = True

    @classmethod
    def from_env(cls) -> "BotConfig":
        return cls(
            telegram_token=os.getenv("TELEGRAM_TOKEN", ""),
            authorized_chat_ids=[
                int(x.strip()) for x in os.getenv("AUTHORIZED_CHAT_IDS", "").split(",") if x.strip()
            ],
            allowed_scopes=[
                x.strip() for x in os.getenv("ALLOWED_SCOPES", "").split(",") if x.strip()
            ],
            log_dir=os.getenv("LOG_DIR", "/app/logs"),
            watchtower_image=os.getenv("WATCHTOWER_IMAGE", "containrrr/watchtower:latest"),
            docker_sock=os.getenv("DOCKER_SOCK", "/var/run/docker.sock"),
        )

    def validate(self) -> None:
        if not self.telegram_token:
            raise ValueError("TELEGRAM_TOKEN does no set")
        if not self.authorized_chat_ids:
            raise ValueError("AUTHORIZED_CHAT_IDS does no set")