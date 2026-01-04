from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_store(docs,user_id:str):
    embeddings = OpenAIEmbeddings()
    # splitter config
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    
    chunks = splitter.split_documents(docs)
    vectordb = Chroma.from_documents(
        embedding=embeddings,
        persist_directory=f"./chroma/{user_id}",
        documents = chunks
    )
    return vectordb
