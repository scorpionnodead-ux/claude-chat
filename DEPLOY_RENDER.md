# Развертывание на Render.com (Полностью бесплатно)

## Шаг 1: Создать аккаунт

1. Перейти на https://render.com
2. Нажать **Get Started for Free**
3. Войти через GitHub (рекомендуется) или Email

## Шаг 2: Подготовить GitHub репозиторий

### Вариант A: Через GitHub Desktop (проще)
1. Скачать GitHub Desktop: https://desktop.github.com
2. Открыть GitHub Desktop
3. File → Add Local Repository → выбрать `C:\scripts\WebControl`
4. Создать новый репозиторий на GitHub
5. Опубликовать (Publish repository)

### Вариант B: Через командную строку
```bash
cd C:\scripts\WebControl

# Инициализировать git
git init

# Добавить файлы
git add .

# Создать коммит
git commit -m "Initial commit: Claude Chat web interface"

# Создать репозиторий на GitHub (нужен GitHub CLI)
gh repo create claude-chat --public --source=. --push
```

## Шаг 3: Развернуть на Render.com

1. Войти на https://dashboard.render.com
2. Нажать **New +** → **Web Service**
3. Подключить GitHub репозиторий `claude-chat`
4. Настройки:
   - **Name**: claude-chat
   - **Runtime**: Docker
   - **Plan**: Free
   - **Branch**: main
5. Нажать **Create Web Service**

## Шаг 4: Дождаться развертывания

- Процесс займет 3-5 минут
- Статус можно отслеживать в логах
- После завершения получите URL: `https://claude-chat-xxxx.onrender.com`

## ✅ Готово!

Ваше приложение доступно по адресу из панели Render.

## 📝 Важные моменты

### Бесплатный тир:
- ✅ Полностью бесплатно (без карты)
- ⏱️ Засыпает после 15 минут неактивности
- 🐌 Пробуждение: ~30-60 секунд
- 💾 750 часов/месяц
- 🔒 Автоматический HTTPS

### Автообновление:
- При push в GitHub → автоматически обновляется на Render
- Можно настроить автодеплой или ручной

## 🔄 Обновление приложения

```bash
cd C:\scripts\WebControl
git add .
git commit -m "Update"
git push
```

Render автоматически задеплоит изменения.

## 🛠️ Полезные ссылки

- Dashboard: https://dashboard.render.com
- Логи: В панели вашего сервиса → Logs
- Настройки: В панели → Settings

## 🐛 Решение проблем

### Долгое пробуждение
- Это нормально для бесплатного тира
- Первый запрос после сна: 30-60 секунд

### Ошибки при деплое
- Проверить логи в Render Dashboard
- Убедиться что все файлы закоммичены в Git

### Приложение не отвечает
- Проверить логи
- Перезапустить: Manual Deploy → Deploy latest commit

---

**Готово! Теперь у вас есть доступ к Claude из любой точки мира!** 🌍
