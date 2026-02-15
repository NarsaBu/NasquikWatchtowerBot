#!/bin/bash
set -e

mkdir -p /app/logs

chown -R botuser:botgroup /app/logs 2>/dev/null || true
chmod -R u+rwx /app/logs 2>/dev/null || true

if [ -S /var/run/docker.sock ]; then
    echo "Docker socket is available"
else
    echo "Docker socket is unavailable"
fi

exec python main.py