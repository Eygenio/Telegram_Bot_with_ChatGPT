import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from config import Config
from chatgpt_client import ChatGPTClient
from database import Database


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()

db = Database()
client = ChatGPTClient()


# HELPER: Клавиатура
def get_main_keyboard():
    keyboard = [
        [types.KeyboardButton(text="🆕 Новый запрос")],
    ]
    return types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id

    # Создаем/обновляем запись пользователя
    db.save_user(user_id)

    # Сбрасываем историю
    db.set_history_id(user_id, None)

    await message.answer(
        "Привет! Я умный ассистент ⚡\n"
        "Задавай вопрос — я отвечу.\n\n"
        "Контекст диалога будет сохраняться автоматически.",
        reply_markup=get_main_keyboard(),
    )


# /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Просто напиши мне сообщение — я отвечу.\n"
        "Нажми «🆕 Новый запрос», чтобы начать новый диалог."
    )


# Кнопка "Новый запрос"
@dp.message(lambda msg: msg.text == "🆕 Новый запрос")
async def new_dialog(message: types.Message):
    user_id = message.from_user.id
    db.set_history_id(user_id, None)

    await message.answer(
        "Диалог начат заново! 🆕\n" "Можешь задавать новый вопрос.",
        reply_markup=get_main_keyboard(),
    )


# Обработка всех сообщений
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text.strip()

    # Убедимся, что пользователь есть в базе данных
    db.save_user(user_id)

    # Получаем сохраненный history_id
    history_id = db.get_history_id(user_id)

    await message.answer("⌛ Думаю...")

    try:
        # Отправляем запрос в ChatGPT
        response_text, new_history_id, response_id = await client.ask(
            prompt=user_text, history_id=history_id
        )

        # Сохраняем новый history_id (если он есть)
        if new_history_id:
            db.set_history_id(user_id, new_history_id)

        # Сохраняем сообщение в историю
        db.save_message(
            user_id=user_id,
            role="user",
            content=user_text,
            history_id=new_history_id or history_id,
            response_id=response_id,
        )
        db.save_message(
            user_id=user_id,
            role="assistant",
            content=response_text,
            history_id=new_history_id or history_id,
            response_id=response_id,
        )

        # Отправляем ответ
        await message.answer(response_text, reply_markup=get_main_keyboard())

    except Exception as e:
        logger.exception(f"Ошибка обработки сообщения: {e}")

        await message.answer(
            "❌ Ошибка при обращении к ChatGPT.\n"
            "Попробуйте снова через несколько секунд."
        )


dp.message()(handle_message)


# main
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
