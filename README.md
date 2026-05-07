# Claude Live Chat - Web Interface

Веб-интерфейс для управления чатом с Claude из любой точки мира.

## 🚀 Быстрый старт (Fly.io - Бесплатно)

### Вариант 1: Автоматическое развертывание
```bash
# Запустить скрипт
deploy_flyio.bat
```

### Вариант 2: Ручное развертывание
```bash
# 1. Установить Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 2. Войти в аккаунт
fly auth login

# 3. Развернуть
cd C:\scripts\WebControl
fly launch
```

## 📱 Возможности

- ✅ Доступ с любого устройства (ПК, телефон, планшет)
- ✅ Красивый адаптивный интерфейс
- ✅ Автообновление чата каждые 3 секунды
- ✅ История сообщений
- ✅ HTTPS из коробки
- ✅ Полностью бесплатно

## 📂 Структура проекта

```
WebControl/
├── server_cloud.py          # Облачная версия сервера
├── server.py                # Локальная версия сервера
├── templates/
│   └── chat.html           # Веб-интерфейс
├── Dockerfile              # Docker конфигурация
├── fly.toml                # Fly.io конфигурация
├── requirements.txt        # Python зависимости
├── deploy_flyio.bat        # Скрипт развертывания
└── DEPLOY_FLYIO.md         # Подробная инструкция
```

## 🌐 Локальный запуск

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
python server_cloud.py

# Открыть в браузере
http://localhost:5000
```

## ☁️ Облачное развертывание

### Fly.io (Рекомендуется)
- **Бесплатно**: 3 VM, 160GB трафика/месяц
- **Автозасыпание**: После 5 минут неактивности
- **Пробуждение**: ~10-15 секунд на первый запрос

```bash
fly launch
fly deploy
fly open
```

### Render.com
- **Бесплатно**: Засыпает после 15 минут
- **Пробуждение**: ~30-60 секунд

### Railway.app
- **$5 кредитов/месяц**: Хватает на ~100 часов работы
- **Без засыпания**: Всегда активен

## 🔧 API Endpoints

### GET /api/chat/recent
Получить последние 20 сообщений
```json
{
  "messages": [
    {
      "type": "human",
      "content": "Привет",
      "timestamp": "2026-05-07T04:30:00"
    }
  ]
}
```

### POST /api/chat/send
Отправить сообщение Claude
```json
{
  "message": "Привет, Claude!"
}
```

### GET /api/commands/pending
Получить список ожидающих команд

### POST /api/commands/clear
Очистить очередь команд

## 📝 Файлы данных

- `chat_history.json` - История сообщений (последние 100)
- `commands.txt` - Очередь команд для Claude

## 🛠️ Полезные команды Fly.io

```bash
fly status              # Статус приложения
fly logs                # Просмотр логов
fly open                # Открыть в браузере
fly deploy              # Обновить приложение
fly scale count 0       # Остановить
fly scale count 1       # Запустить
fly apps destroy        # Удалить приложение
```

## 🔒 Безопасность

⚠️ **Важно**: Текущая версия не имеет аутентификации!

Для продакшена добавьте:
- Базовую HTTP аутентификацию
- OAuth (Google, GitHub)
- API ключи
- Rate limiting

## 📊 Мониторинг

```bash
# Просмотр логов в реальном времени
fly logs -a claude-chat

# Статус и метрики
fly status -a claude-chat

# SSH доступ к контейнеру
fly ssh console -a claude-chat
```

## 🐛 Решение проблем

### Приложение не запускается
```bash
fly logs
fly apps restart claude-chat
```

### Долгое пробуждение
- Это нормально для бесплатного тира
- Первый запрос после засыпания: ~10-15 сек

### Ошибки при развертывании
```bash
# Проверить конфигурацию
fly config validate

# Пересоздать приложение
fly apps destroy claude-chat
fly launch
```

## 📞 Поддержка

- Fly.io документация: https://fly.io/docs
- Fly.io community: https://community.fly.io

## 📄 Лицензия

MIT License - используйте свободно!

---

**Создано для удобного управления Claude из любой точки мира** 🌍
