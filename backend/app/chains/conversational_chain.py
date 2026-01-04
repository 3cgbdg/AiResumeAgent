from langchain_pinecone import PineconeVectorStore
from os import getenv
from dotenv import load_dotenv
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI
from ..core.llm import llm

load_dotenv()

# storing users chat history
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def create_conversational_chain(user_id: str):
    vectordb = PineconeVectorStore.from_existing_index(
        index_name=getenv("INDEX_NAME"),
        embedding=OpenAIEmbeddings(),
        namespace=user_id,
    )
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
    You are an AI recruiter.
    Answer the question using ONLY the context below.

    Context:
    {context}"""),
        ("placeholder", "{chat_history}"),
        ("human", "{question}")
    ])

    chain = (
        {
            "context": (lambda x: x["question"]) | retriever,
            "question": lambda x: x["question"]
        }
        | prompt
        | llm
    )
    
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
    
    return chain_with_history