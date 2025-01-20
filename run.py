import os
import asyncio
import logging

from aiogram import Bot, Dispatcher

from dotenv import load_dotenv

from app.handlers import router
from app.database.models import create_db_and_tables

async def main():
    await create_db_and_tables()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt):
        print("Bot stopped")
