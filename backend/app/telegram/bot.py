from aiogram import Bot, Dispatcher
from aiogram.types import Message
from os import getenv,remove
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from ..rag.resume_loader import load_resume
from ..rag.vector_store import create_vector_store

load_dotenv()

bot = Bot(token=getenv("BOT_TOKEN"))
dp=Dispatcher()

# catching doc having pdf type

@dp.message(lambda msg : msg.document and msg.document.mime_type == "application/pdf"):
async def handle_pdf(message:Message):
    user_id = str(message.from_user.id)
    
    file = await bot.get_file(message.document.file_id)
    # sending logger into tg chat 
    await message.answer("PDF has been ")
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        await bot.download_file(file.file_path, tmp)
        file_path = tmp.name
    docs = load_resume(file_path)
    create_vector_store(docs,user_id)
    remove(file_path)
    await message.answer("PDF has been uploaded")
    
    
  
    
        
