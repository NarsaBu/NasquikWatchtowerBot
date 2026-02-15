import os
from typing import List
from pydantic import BaseModel, Field, ValidationError


class BotConfig(BaseModel):
    telegram_token: str = Field(..., description="Telegram bot token")
    authorized_chat_ids: List[int] = Field(default_factory=list, description="Authorized chat_ids")
    allowed_scopes: List[str] = Field(default_factory=list, description="Allowed scopes")
    log_dir: str = Field(default="/app/logs", description="Log directory")
    watchtower_image: str = Field(default="containrrr/watchtower:latest", description="Watchtower image")
    docker_sock: str = Field(default="/var/run/docker.sock", description="Docker socket path")

    @classmethod
    def from_env(cls) -> "BotConfig":
        try:
            config = cls(
                telegram_token=os.environ["TELEGRAM_TOKEN"],
                authorized_chat_ids=[
                    int(x.strip()) for x in os.environ.get("AUTHORIZED_CHAT_IDS", "").split(",") if x.strip()
                ],
                allowed_scopes=[
                    x.strip() for x in os.environ.get("ALLOWED_SCOPES", "").split(",") if x.strip()
                ],
                log_dir=os.environ.get("LOG_DIR", "/app/logs"),
                watchtower_image=os.environ.get("WATCHTOWER_IMAGE", "containrrr/watchtower:latest"),
                docker_sock=os.environ.get("DOCKER_SOCK", "/var/run/docker.sock"),
            )
            config._assert_valid()
            return config
        except KeyError as e:
            raise ValueError(f"Required environment variable does not set: {e}")
        except ValidationError as e:
            raise ValueError(f"Configuration valudation error: {e}")
        except Exception as e:
            raise ValueError(f"Configuration creation error: {e}")

    def _assert_valid(self) -> None:
        if not self.telegram_token:
            raise ValueError("TELEGRAM_TOKEN does not set")
        if not self.authorized_chat_ids:
            raise ValueError("AUTHORIZED_CHAT_IDS does no set")