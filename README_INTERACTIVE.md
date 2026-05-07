# Claude Code Web Interface v2

Двусторонний веб-интерфейс для Claude Code CLI с поддержкой интерактивного общения.

## Возможности

✅ **Live View** - просмотр текущего разговора в реальном времени
✅ **Interactive Chat** - отправка сообщений в CLI через веб
✅ **Permission Requests** - ответы на запросы разрешений через веб (в разработке)
✅ **Удалённый доступ** - через ngrok доступно из любой точки мира

## Быстрый старт

### Запуск всех сервисов

```bash
start_interactive.bat
```

Это запустит:
- Flask сервер на порту 8080
- Ngrok туннель для удалённого доступа

### Доступные интерфейсы

**Локально:**
- Live View: http://localhost:8080/live
- Interactive Chat: http://localhost:8080/chat

**Удалённо (через ngrok):**
- Получите URL из вывода скрипта или откройте http://localhost:4040

## Как это работает

### 1. Live View (`/live`)
- Показывает историю сообщений из `chat_history.json`
- Автоматически обновляется каждые 2 секунды
- Только для просмотра

### 2. Interactive Chat (`/chat`)
- Отправляйте сообщения Claude через веб
- Сообщения сохраняются в `chat_history.json`
- Добавляются в очередь `pending_messages.json` для CLI

### 3. Bridge (в разработке)
Скрипт `bridge.py` будет автоматически передавать сообщения из веб в CLI:

```bash
python bridge.py
```

## Структура файлов

```
WebControl/
├── unified_server_v2.py      # Основной Flask сервер
├── bridge.py                  # Мост веб → CLI (в разработке)
├── start_interactive.bat      # Скрипт запуска
├── chat_history.json          # История сообщений
├── pending_messages.json      # Очередь сообщений для CLI
├── permission_requests.json   # Запросы разрешений
└── templates/
    ├── live_chat.html         # Live View интерфейс
    └── interactive_chat.html  # Interactive Chat интерфейс
```

## API Endpoints

### GET /api/messages
Получить историю сообщений

### POST /api/send
Отправить сообщение в CLI
```json
{
  "message": "Ваше сообщение"
}
```

### GET /api/pending-messages
Получить необработанные сообщения (для CLI)

### POST /api/mark-processed
Отметить сообщение как обработанное

### GET /api/permission-requests
Получить активные запросы разрешений

### POST /api/answer-permission
Ответить на запрос разрешения
```json
{
  "request_id": "...",
  "answer": "yes" // или "no"
}
```

## Roadmap

- [x] Live View интерфейс
- [x] Отправка сообщений из веб
- [x] Сохранение истории
- [ ] Автоматическая передача в CLI
- [ ] Обработка запросов разрешений
- [ ] WebSocket для real-time обновлений
- [ ] Аутентификация

## Технологии

- Flask + Flask-CORS
- Vanilla JavaScript
- Ngrok для туннелирования
- JSON для хранения данных
