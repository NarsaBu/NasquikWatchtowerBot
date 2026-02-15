import os
from typing import List
from pydantic import BaseModel, Field, ValidationError

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
        try:
            return cls(
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
        except KeyError as e:
            raise ValueError(f"Required environment variable is not set.: {e}")
        except ValidationError as e:
            raise ValueError(f"Configuration validation error: {e}")