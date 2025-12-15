from aiogram import Bot, Dispatcher, executor, types
from app.config import BOT_TOKEN
from app.db import get_connection
from app.nlp import parse_intent
from app.queries import build_query

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def handle_message(message: types.Message):
    intent = parse_intent(message.text)
    query, params = build_query(intent)

    if not query:
        await message.answer("0")
        return

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    await message.answer(str(result))

if __name__ == "__main__":
    executor.start_polling(dp)
