import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

    # Database
    DATABASE_NAME = os.getenv("DATABASE_NAME", "database.db")

    # Параметры генерации
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1000"))

    # Проверка обязательных переменных
    if not BOT_TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN не найден в .env")

    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY не найден в .env")
