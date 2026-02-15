FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 botuser && \
    mkdir -p /app/logs && \
    chown -R botuser:botuser /app

WORKDIR /app

COPY --chown=botuser:botuser requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

COPY --chown=botuser:botuser . .

USER botuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; exit(0)" || exit 1

CMD ["python", "main.py"]