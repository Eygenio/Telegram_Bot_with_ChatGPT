import sqlite3
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Database:
    def __init__(self, path: str = "database.db"):
        self.path = path
        self._create_tables()

    # CONNECT
    def _connect(self):
        return sqlite3.connect(self.path)

    # CREATE TABLET
    def _create_tables(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()

                # Таблица пользователей
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        history_id TEXT
                    )
                """
                )

                # Таблица сообщений
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        role TEXT,
                        content TEXT,
                        history_id TEXT,
                        response_id,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Ошибка при создании таблицы: {e}")

    # USER OPERATIONS
    def save_user(self, user_id: int):
        """
        Добавляем пользователя, если его нет.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()

                cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
                exists = cursor.fetchone()

                if not exists:
                    cursor.execute(
                        "INSERT INTO users(user_id, history_id) VALUES (?, ?)",
                        (user_id, None)
                    )
                    conn.commit()

        except Exception as e:
            logger.error(f"Ошибка save_user: {e}")

    def set_history_id(self, user_id: int, history_id: Optional[str]):
        """
        Сохраняет history_id пользователя.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET history_id=? WHERE user_id=?",
                    (history_id,user_id)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Ошибка set_history_id: {e}")
            return None

    def get_history_id(self, user_id: int) -> Optional[str]:
        """
        Возвращает history_id пользователя.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT history_id FROM users WHERE user_id=?", (user_id,)
                )
                row = cursor.fetchone()
                return row[0] if row else None

        except Exception as e:
            logger.error(f"Ошибка get_history_id: {e}")
            return None

    # SAVE MESSAGE
    def save_message(
        self,
        user_id: int,
        role: str,
        content: str,
        history_id: Optional[str],
        response_id: Optional[str]
    ):
        """
        Сохраняет сообщения.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO messages (user_id, role, content, history_id, response_id)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, role, content, history_id, response_id)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Ошибка save_message: {e}")
