#!/bin/bash
set -e

mkdir -p /app/logs
chown -R botuser:botgroup /app/logs
chmod -R u+rwx /app/logs

if [ -S /var/run/docker.sock ]; then
    echo "Docker socket is available"
    chmod o+rw /var/run/docker.sock 2>/dev/null || true
else
    echo "Docker socket is unavailable"
fi

exec su - botuser -c "cd /app && python main.py"