FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*

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