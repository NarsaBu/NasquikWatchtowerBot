#!/bin/bash
set -e

echo "=== CONTAINER IS RUNNING ==="
echo "User: $(whoami) (UID=$(id -u))"
echo "PATH: $PATH"
echo "Docker: $(which docker || echo 'IS NOT FOUND')"
docker --version 2>/dev/null || echo "Docker CLI is not available!"

mkdir -p /app/logs

if [ -S /var/run/docker.sock ]; then
    echo "✓ Docker socket is available"
    ls -la /var/run/docker.sock | awk '{print "  Rights:", $1, "Owner:", $3}'
else
    echo "Docker socket is not available"
fi
echo "========================="

exec python main.py