# Stage 1: build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: runtime
FROM python:3.11-slim

# Docker CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 botuser && \
    mkdir -p /app/logs && \
    chown -R botuser:botuser /app

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY --chown=botuser:botuser bot.py .
COPY --chown=botuser:botuser requirements.txt .

USER botuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; r = requests.get('https://api.telegram.org/bot${TELEGRAM_TOKEN}/getMe'); exit(0 if r.status_code == 200 else 1)" || exit 1

CMD ["python", "bot.py"]