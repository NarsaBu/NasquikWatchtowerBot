import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import aiofiles

class LogRepository:

    def __init__(self, log_dir: str):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    async def create_log_file(self, scope: str, is_check: bool) -> str:
        mode = "check" if is_check else "update"
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{mode}_{scope}_{timestamp}.log"
        return str(self.log_dir / filename)

    async def save_line(self, log_path: str, line: str) -> None:
        async with aiofiles.open(log_path, 'a') as f:
            await f.write(line + '\n')
            await f.flush()

    def get_recent_logs(self, limit: int = 5) -> List[Tuple[str, int, str]]:
        logs = []
        for f in sorted(self.log_dir.glob('*.log'), key=lambda x: x.stat().st_mtime, reverse=True):
            if f.name == 'bot.log':
                continue
            logs.append((
                f.name,
                f.stat().st_size,
                datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            ))
            if len(logs) >= limit:
                break
        return logs