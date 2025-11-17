# 🤖 Telegram ChatGPT Bot — Ассистент с памятью диалогов

Интеллектуальный Telegram-бот, использующий **OpenAI Responses API** с поддержкой `history_id` для сохранения контекста диалога.  
Бот ведёт полноценные «беседы» и запоминает, о чём говорилось ранее.

---

## ✨ Особенности

- 💬 **Контекстные диалоги** (через `history_id`)
- 🔄 **Перезапуск диалога** по кнопке "🆕 Новый запрос"
- 🧠 **Сохранение всех сообщений** в SQLite
- ⚡ Полностью асинхронная работа (`aiogram + aiohttp`)
- 🐳 Готовая сборка через **Docker** и `docker-compose`
- 🔐 Поддержка `.env` и безопасного хранения ключей
- 🗂️ Простая и понятная архитектура

---

## 🏗️ Архитектура проекта

- **Aiogram 3.4** — современный Telegram-фреймворк  
- **OpenAI Responses API** — модель с историей (`history_id`)  
- **SQLite** — база данных для пользователей и сообщений  
- **AIOHTTP** — асинхронные запросы к OpenAI  
- **Docker + docker-compose** — автоматический деплой и перезапуск  

Файлы проекта:

```
project/
 ├── bot.py
 ├── chatgpt_client.py
 ├── config.py
 ├── database.py
 ├── requirements.txt
 ├── Dockerfile
 ├── docker-compose.yml
 └── README.md
```

---

## 💡 Функциональность

### 👤 Для пользователей
- Отправка сообщений боту
- Получение ответов модели ChatGPT
- Контекст диалога сохраняется между сообщениями
- Возможность начать новый диалог по кнопке
- Красивые кнопки и минимальный интерфейс

### 🛠️ Для разработчиков
- Хранение истории пользователя (`history_id`)
- Логирование всех сообщений в SQLite
- Минимальные зависимости
- Простая интеграция в любые проекты
- Лёгкий деплой в Docker

---

## 🚀 Запуск проекта (локально)

### 1. Клонировать репозиторий
```bash
git clone https://github.com/yourname/chatgpt_telegram_bot
cd chatgpt_telegram_bot
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Создать файл `.env`
```env
TELEGRAM_TOKEN=ваш_telegram_токен
OPENAI_API_KEY=ваш_openai_ключ
OPENAI_MODEL=gpt-4.1
```

### 4. Запустить бота
```bash
python bot.py
```

---

## 🐳 Запуск через Docker

### 1. Собрать контейнер
```bash
docker-compose build
```

### 2. Запустить
```bash
docker-compose up -d
```

### 3. Посмотреть логи
```bash
docker-compose logs -f
```

Бот автоматически перезапускается при авариях.

---

## 📦 Структура данных в SQLite

### Таблица `users`
| user_id | history_id |
|--------|------------|

### Таблица `messages`
| id | user_id | role | content | history_id | response_id | timestamp |

---

## ⚙️ Использование OpenAI Responses API

Запросы отправляются на:
```
POST https://api.openai.com/v1/responses
```

Для продолжения диалога передаётся:
```json
{
  "model": "gpt-4.1",
  "input": "Сообщение",
  "history_id": "prev_history_id",
  "store": true
}
```

Модель возвращает новый `history_id`, который сохраняется в БД.

---

## 🔐 Безопасность

- Все токены хранятся только в `.env`
- Ключи не записываются в логи
- SQLite изолирован внутри контейнера (если ты используешь Docker)

---
