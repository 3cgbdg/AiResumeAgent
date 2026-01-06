from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from ...chains.conversational_chain import create_conversational_chain


# chat messaging question -> ai response
def register_ainswer_handler(dp:Dispatcher):
    @dp.message(F.text)
    async def handle_pdf(message: Message):
        user_id = str(message.from_user.id)
        text = message.text
        if text:
            await message.answer("Wait for the answer...")
        else:
            raise RuntimeError("Something went wrong!")
        chain = create_conversational_chain(user_id)
        response = await chain.ainvoke(
        {"question": text},  
        config={"configurable": {"session_id": user_id}}
        )
        await message.answer(response.content)