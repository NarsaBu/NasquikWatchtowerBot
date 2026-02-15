#!/bin/bash
set -e

mkdir -p /app/logs

if [ -S /var/run/docker.sock ]; then
    echo "✓ Docker socket is available"
else
    echo "⚠️ Docker socket is not available"
fi

exec python main.py