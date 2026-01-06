from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from os import remove
from tempfile import NamedTemporaryFile
from ...rag.resume_loader import load_resume
from ...rag.vector_store import create_vector_store


dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Hello! Send me a PDF resume to upload it.")


# catching doc having pdf type

@dp.message(F.document.mime_type == "application/pdf")
async def handle_pdf(message: Message):
    user_id = str(message.from_user.id)

    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        await message.bot.download(message.document, destination=tmp.name)
        file_path = tmp.name
    docs = load_resume(file_path)
    create_vector_store(docs, user_id)
    remove(file_path)
    await message.answer("PDF has been uploaded")
