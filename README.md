# Nasquik Watchtower Telegram Bot

Управление обновлениями Docker-контейнеров с помощью Watchtower через Telegram с живыми логами.

## Требования безопасности

1. **Только авторизованные пользователи** — бот проверяет `chat_id`
2. **Валидация имён групп** — только буквы/цифры/дефисы
3. **Белый список групп** — обновление только разрешённых `scope`
4. **Нет прямого выполнения команд** — все параметры валидируются

## Развертывание

### Шаг 1: Подготовка кода на сервере

1. Создать директорию проекта
   ```
   mkdir -p /opt/nasquik-watchtower-bot
   cd /opt/nasquik-watchtower-bot
   ```
2. Скопировать ВСЕ файлы проекта (scp or git clone)

### Шаг 2. Сбока образа на сервере

```
cd /opt/watchtower-bot
docker build -t nasquik-watchtower-bot:latest .
```

### Шаг 3. Создать стек через Portainer (Web editor)

docker-compose.yml для стека
```
version: '3.8'
services:
  nasquik-watchtower-bot:
    image: nasquik-watchtower-bot:latest
    container_name: nasquik-watchtower-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_TOKEN=8400087115:AAGSdIji5t6htxNt5zj5EBwaYAjXXqf3zCk
      - AUTHORIZED_CHAT_IDS=61581878,51374704
      - ALLOWED_SCOPES=diun,jellyfin,komga,navidrome,photoprism,npm,qbittorrent,watchtower
      - TZ=Europe/Moscow
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /opt/nasquik-watchtower-bot/logs:/app/logs
      - /usr/bin/docker:/usr/bin/docker:ro
    user: "1000:994"
```
При обновлении кода:
```
cd /opt/nasquik-watchtower-bot
docker build -t nasquik-watchtower-bot:latest . --no-cache
```
В Portainer: Stacks → nasquik-watchtower-bot → Recreate