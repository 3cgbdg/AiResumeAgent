from fastapi import APIRouter
from .schemas.chat import ChatRequest
from ..chains.conversational_chain import create_conversational_chain
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_with_resume(req: ChatRequest):

    chain = create_conversational_chain(req.user_id)
    response = await chain.ainvoke(
    {"question": req.question},  
    config={"configurable": {"session_id": req.user_id}}
    )

    return {"answer": response.content}
