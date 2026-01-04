from ..core.llm import llm
from fastapi import APIRouter
from .schemas.chat import ChatRequest
from langchain_chroma import Chroma
from langchain_community.chains import PebbloRetrievalQA
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_with_resume(req: ChatRequest):
    vectordb = Chroma(
        embedding_function=OpenAIEmbeddings(),
        persist_directory=f"./chroma/{req.user_id}",
    )
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    qa_chain = PebbloRetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        app_name="AI Recruiter",
        description="RAG QA chain for candidate resumes",
        owner=getenv("OWNER_NAME"),
    )
    result = qa_chain.run(req.question)

    return {"answer": result}
