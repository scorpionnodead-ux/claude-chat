# Развертывание Claude Chat на Fly.io (Бесплатно)

## Шаг 1: Установка Fly CLI

### Windows:
```bash
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Linux/Mac:
```bash
curl -L https://fly.io/install.sh | sh
```

## Шаг 2: Регистрация и вход

```bash
# Зарегистрироваться (откроется браузер)
fly auth signup

# Или войти если уже есть аккаунт
fly auth login
```

## Шаг 3: Развертывание приложения

```bash
# Перейти в папку проекта
cd C:\scripts\WebControl

# Запустить развертывание
fly launch

# Ответить на вопросы:
# - App name: claude-chat (или свое имя)
# - Region: выбрать ближайший (ams - Amsterdam, fra - Frankfurt)
# - PostgreSQL: No
# - Redis: No
# - Deploy now: Yes
```

## Шаг 4: После развертывания

Ваше приложение будет доступно по адресу:
```
https://claude-chat.fly.dev
```

## Полезные команды:

```bash
# Посмотреть статус
fly status

# Посмотреть логи
fly logs

# Открыть приложение в браузере
fly open

# Обновить приложение после изменений
fly deploy

# Остановить приложение
fly scale count 0

# Запустить снова
fly scale count 1

# Удалить приложение
fly apps destroy claude-chat
```

## Бесплатный тир включает:

- 3 shared-cpu-1x VMs (256MB RAM)
- 160GB bandwidth/месяц
- Автоматический HTTPS
- Глобальная CDN

## Важно:

1. **Автоматическое засыпание**: Приложение засыпает после 5 минут неактивности
2. **Первый запрос медленный**: ~10-15 секунд на пробуждение
3. **Данные сохраняются**: chat_history.json и commands.txt сохраняются между перезапусками

## Проблемы?

```bash
# Проверить логи
fly logs

# Перезапустить
fly apps restart claude-chat

# SSH в контейнер
fly ssh console
```

## Альтернативные регионы:

- ams (Amsterdam) - Европа
- fra (Frankfurt) - Европа
- lhr (London) - Европа
- iad (Virginia) - США Восток
- lax (Los Angeles) - США Запад
- sin (Singapore) - Азия
- syd (Sydney) - Австралия
