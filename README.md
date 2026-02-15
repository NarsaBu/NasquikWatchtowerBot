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

### Шаг 2. Создание стека в Portainer (делается ОДИН раз)

1. Откройте Portainer → Stacks → Add stack 
2. Заполните поля:
   1. **Name:** watchtower-bot 
   2. **Build method:** Build new image 
   3. **Dockerfile:** path Dockerfile (относительный путь от контекста)
   4. **Context:** /opt/watchtower-bot (путь к директории с проектом на сервере)
   5. **Environment variables:**
      ```
      Вставьте ваши секреты: TELEGRAM_TOKEN=... AUTHORIZED_CHAT_IDS=... ALLOWED_SCOPES=qbittorrent,jellyfin,...
      ```
3. Нажмите Deploy the stack. Portainer автоматически:
   1. Прочитает Dockerfile 
   2. Соберёт образ (docker build)
   3. Запустит контейнер с вашими переменными окружения 
   4. Смонтирует тома (/var/run/docker.sock, ./logs)