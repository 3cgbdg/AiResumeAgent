from ..core.llm import llm
from fastapi import APIRouter
from .schemas.chat import ChatRequest
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_with_resume(req: ChatRequest):
    vectordb = PineconeVectorStore.from_existing_index(
        index_name="resume-index",
        embedding=OpenAIEmbeddings(),
        namespace=req.user_id,
    )
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    prompt = ChatPromptTemplate.from_template("""
    You are an AI recruiter.
    Answer the question using ONLY the context below.

    Context:
    {context}

    Question:
    {question}
    """)

    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )

    result = chain.invoke(req.question)   

    return {"answer": result.content}