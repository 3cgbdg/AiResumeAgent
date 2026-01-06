from os import getenv
import asyncio
from dotenv import load_dotenv
from aiogram import Bot
from .handlers.handle_pdf import dp
load_dotenv()


async def main():
    bot = Bot(token=getenv("BOT_TOKEN"))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
