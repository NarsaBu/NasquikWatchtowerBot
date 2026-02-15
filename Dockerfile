FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g ${GROUP_ID} botgroup && \
    useradd -u ${USER_ID} -g botgroup -m botuser && \
    mkdir -p /app/logs && \
    chown -R botuser:botgroup /app/logs

COPY --chown=botuser:botgroup requirements.txt .
USER botuser
RUN pip install --user --no-cache-dir -r requirements.txt
ENV PATH="/home/botuser/.local/bin:${PATH}"

USER root
COPY --chown=botuser:botgroup . .
RUN chown -R botuser:botgroup /app

COPY --chown=botuser:botgroup entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN chown -R botuser:botgroup /app

USER botuser

ENTRYPOINT ["/app/entrypoint.sh"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)" || exit 1

CMD ["python", "main.py"]