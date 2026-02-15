FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN useradd -m -u 1000 botuser

COPY --chown=botuser:botuser requirements.txt .
USER botuser
RUN pip install --user --no-cache-dir -r requirements.txt
ENV PATH="/home/botuser/.local/bin:${PATH}"

USER root
COPY --chown=botuser:botuser . .
RUN mkdir -p /app/logs && chown -R botuser:botuser /app

USER botuser

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["python", "main.py"]