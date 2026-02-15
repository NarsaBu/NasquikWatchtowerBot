FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN groupadd -g 1000 botgroup && \
    useradd -u 1000 -g botgroup -m botuser && \
    mkdir -p /app/logs && \
    chown -R botuser:botgroup /app/logs

COPY --chown=botuser:botgroup requirements.txt .
USER botuser
ENV PATH="/home/botuser/.local/bin:/usr/local/bin:/usr/bin:/bin:${PATH}"
RUN pip install --user --no-cache-dir -r requirements.txt

USER root
COPY --chown=botuser:botgroup . .
RUN chown -R botuser:botgroup /app

COPY --chown=botuser:botgroup entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER botuser
ENTRYPOINT ["/app/entrypoint.sh"]