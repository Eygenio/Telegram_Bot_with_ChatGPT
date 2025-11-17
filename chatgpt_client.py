import aiohttp
import logging
from typing import Optional, Tuple

from config import Config

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class ChatGPTClient:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        self.api_url = "https://api.openai.com/v1/responses"

    async def ask(
        self,
        prompt: str,
        history_id: Optional[str] = None
    ) -> Tuple[str, Optional[str], Optional[str]]:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "input": prompt,
            "store": True
        }

        if history_id:
            payload["history_id"] = history_id

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=payload) as resp:
                    data = await resp.json()

                    if resp.status != 200:
                        logger.error(f"OpenAI API error {resp.status}: {data}")
                        raise Exception(f"OpenAI API error {data}")

                    # Извлекаем текст
                    text = data["output"][0]["content"][0]["text"]

                    # Новый history_id (если появился)
                    new_history_id = data.get("history_id")

                    # Текущий response_id
                    response_id = data.get("id")

                    return text, new_history_id, response_id

        except Exception as e:
            logger.error(f"Ошибка при запросе к OpenAI API: {e}")
            raise Exception("Ошибка соединения с OpenAI API") from e
