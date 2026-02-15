import asyncio
import subprocess
from typing import AsyncGenerator
from core.exceptions import DockerCommandError


class DockerService:

    def __init__(self, docker_sock: str, watchtower_image: str):
        self.docker_sock = docker_sock
        self.watchtower_image = watchtower_image

    async def run_watchtower(
            self,
            scope: str,
            is_check: bool = False
    ) -> AsyncGenerator[str, None]:
        cmd = [
            'docker', 'run', '--rm',
            '-v', f'{self.docker_sock}:{self.docker_sock}',
            self.watchtower_image,
            '--run-once',
            '--scope', scope,
            '--cleanup',
            '--debug'
        ]
        if is_check:
            cmd.append('--monitor-only')

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        while True:
            line = await process.stdout.readline()
            if not line:
                break
            yield line.decode('utf-8', errors='replace').rstrip()

        await process.wait()

        if process.returncode != 0:
            raise DockerCommandError(f"Watchtower finished with code {process.returncode}")