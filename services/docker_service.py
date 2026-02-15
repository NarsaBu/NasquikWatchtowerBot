import asyncio
import subprocess
from typing import Tuple
from pathlib import Path
from core.exceptions import DockerCommandError


class DockerService:

    def __init__(self, docker_sock: str, watchtower_image: str):
        self.docker_sock = docker_sock
        self.watchtower_image = watchtower_image

    async def run_watchtower(
            self,
            scope: str,
            log_path: str,
            is_check: bool = False
    ) -> Tuple[bool, str, int]:
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

        with open(log_path, 'a') as f:
            f.write(f"Starting command: {' '.join(cmd)}\n")
            f.flush()

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        output_lines = []
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            decoded = line.decode('utf-8', errors='replace').rstrip()
            output_lines.append(decoded)

            with open(log_path, 'a') as f:
                f.write(decoded + '\n')
                f.flush()

        await process.wait()

        success = process.returncode == 0
        updated_count = 0
        found_update = False

        for line in output_lines[-50:]:  # last 50 lines to analysis
            if 'Updated=' in line:
                try:
                    parts = line.split('Updated=')
                    if len(parts) > 1:
                        updated_count = int(parts[1].split()[0])
                except:
                    pass
            if 'Found new image' in line or 'Found updated' in line:
                found_update = True

        if not success:
            summary = f"Error while processing update (code {process.returncode})"
        elif is_check:
            if found_update:
                summary = "Updates detected"
            else:
                summary = "Everything is up-to-date"
        else:
            if updated_count > 0:
                summary = f"Successfully updated containers: {updated_count}"
            else:
                summary = "Nothing to update"

        return success, summary, updated_count