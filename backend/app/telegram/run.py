from os import getenv
import asyncio
from dotenv import load_dotenv
from aiogram import Bot,Dispatcher
from .handlers.handle_pdf import  register_pdf_handler
from .handlers.handle_ainswer import register_ainswer_handler
load_dotenv()


async def main():
    bot = Bot(token=getenv("BOT_TOKEN"))
    dp = Dispatcher()
    register_ainswer_handler(dp)
    register_pdf_handler(dp)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
    
