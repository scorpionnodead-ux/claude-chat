# 🚀 Быстрый старт: Развертывание на Render.com

## ✅ Что уже готово:
- [x] Git репозиторий инициализирован
- [x] Все файлы добавлены и закоммичены
- [x] Dockerfile настроен
- [x] render.yaml создан

## 📋 Что нужно сделать (5 минут):

### Шаг 1: Создать GitHub репозиторий

1. Откройте: **https://github.com/new**
2. Заполните:
   - Repository name: `claude-chat`
   - Description: `Web interface for Claude chat`
   - Visibility: **Public** ✓
   - **НЕ** ставьте галочки на README, .gitignore, license
3. Нажмите **Create repository**

### Шаг 2: Загрузить код на GitHub

GitHub покажет команды. Скопируйте и выполните их:

```bash
cd C:\scripts\WebControl

# Замените YOUR_USERNAME на ваш GitHub username
git remote add origin https://github.com/YOUR_USERNAME/claude-chat.git
git branch -M main
git push -u origin main
```

**Или используйте эти команды напрямую:**

```bash
cd C:\scripts\WebControl
git remote add origin https://github.com/YOUR_USERNAME/claude-chat.git
git branch -M main
git push -u origin main
```

### Шаг 3: Развернуть на Render.com

1. Откройте: **https://dashboard.render.com**
2. Войдите через GitHub (если еще не вошли)
3. Нажмите **New +** → **Web Service**
4. Найдите репозиторий `claude-chat` и нажмите **Connect**
5. Настройки:
   - **Name**: `claude-chat` (или свое имя)
   - **Runtime**: Docker
   - **Branch**: main
   - **Plan**: **Free** ✓
6. Нажмите **Create Web Service**

### Шаг 4: Дождаться развертывания

- Процесс займет **3-5 минут**
- Следите за логами в реальном времени
- Когда увидите "Build successful" → готово!

### Шаг 5: Получить URL

После завершения развертывания:
- URL будет вверху страницы: `https://claude-chat-xxxx.onrender.com`
- Скопируйте и сохраните его
- Откройте в браузере

## 🎉 Готово!

Теперь вы можете:
- Открыть чат с любого устройства
- Добавить в закладки на телефоне
- Отправлять команды Claude из любой точки мира

## 📱 Использование

1. Откройте URL в браузере
2. Введите сообщение в поле ввода
3. Нажмите Send или Enter
4. Сообщение отправится Claude

## ⚠️ Важно знать

- **Засыпание**: Приложение засыпает через 15 минут неактивности
- **Пробуждение**: Первый запрос после сна займет ~30-60 секунд
- **Лимиты**: 750 часов/месяц (более чем достаточно)
- **HTTPS**: Автоматически включен

## 🔄 Обновление приложения

Если внесли изменения в код:

```bash
cd C:\scripts\WebControl
git add .
git commit -m "Update: описание изменений"
git push
```

Render автоматически задеплоит обновление.

## 🆘 Нужна помощь?

- **Логи**: Dashboard → Logs
- **Перезапуск**: Manual Deploy → Deploy latest commit
- **Настройки**: Settings → Environment

---

**Время выполнения: ~5 минут**
**Стоимость: $0 (полностью бесплатно)**
