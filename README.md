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
      - TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
      - AUTHORIZED_CHAT_IDS=${AUTHORIZED_CHAT_IDS}
      - ALLOWED_SCOPES=${ALLOWED_SCOPES}
      - TZ=Europe/Moscow
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /opt/watchtower-bot/logs:/app/logs  # ← АБСОЛЮТНЫЙ ПУТЬ НА ХОСТЕ
    user: "1000:1000"  # ← UID:GID вашего пользователя
```
При обновлении кода:
```
cd /opt/nasquik-watchtower-bot
docker build -t nasquik-watchtower-bot:latest . --no-cache
```
В Portainer: Stacks → nasquik-watchtower-bot → Recreate