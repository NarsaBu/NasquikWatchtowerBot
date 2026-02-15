# Nasquik Watchtower Telegram Bot

Управление обновлениями Docker-контейнеров с помощью Watchtower через Telegram с живыми логами.

## Требования безопасности

1. **Только авторизованные пользователи** — бот проверяет `chat_id`
2. **Валидация имён групп** — только буквы/цифры/дефисы
3. **Белый список групп** — обновление только разрешённых `scope`
4. **Нет прямого выполнения команд** — все параметры валидируются

## Подготовка к использованию

### Шаг 1. Подготовка файлов на сервере

Создать директорию
```
mkdir -p /opt/watchtower-bot/logs
cd /opt/watchtower-bot
```

Скачать/создать файлы (Dockerfile, docker-compose.yml, bot.py, requirements.txt)
... (скопировать содержимое из этого ответа)

Создать .env с вашими данными
```
cp .env.example .env
nano .env  # ← ВСТАВИТЬ СВОЙ ТОКЕН И CHAT_ID
```

### Шаг 2. Настройка прав

Дать права на запись логов
```
sudo chown -R 1000:1000 /opt/watchtower-bot/logs
```

Проверить группу docker (обычно gid=999 или 1001)
```
ls -la /var/run/docker.sock
```
Если группа не 999 — запомните реальный GID для следующего шага


### Шаг 3: Создать стек в Portainer

1. Stacks → Add stack
2. Имя: watchtower-bot 
3. В поле Repository укажите путь: /opt/watchtower-bot
4. В Environment variables добавьте:
   ```
   TELEGRAM_TOKEN=ваш_токен
   AUTHORIZED_CHAT_IDS=ваш_chat_id
   ALLOWED_SCOPES=qbittorrent,jellyfin,...
   ```
5. Нажмите Deploy the stack. Важно: Если контейнер не может запустить docker команды, добавьте в docker-compose.yml: ```user: "1000:999"  # UID:GID вашей группы docker```
