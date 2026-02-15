from typing import Optional, List
from pydantic import BaseModel

class UpdateResult(BaseModel):
    scope: str
    is_check: bool
    success: bool
    log_path: str
    summary: str
    lines_count: int

class LogEntry(BaseModel):
    filename: str
    size_bytes: int
    timestamp: str

class TelegramUser(BaseModel):
    chat_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None