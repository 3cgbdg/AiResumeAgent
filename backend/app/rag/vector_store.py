from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from pinecone import ServerlessSpec
from os import getenv
from ..core.pinecone import get_pinecone_client

load_dotenv()

index_name = getenv("INDEX_NAME")

pc = get_pinecone_client()

#   if index hasn`t been created yet

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


def create_vector_store(docs, user_id: str):

    embeddings = OpenAIEmbeddings()
    # splitter config
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)

    chunks = splitter.split_documents(docs)
    vectordb = PineconeVectorStore.from_documents(
        embedding=embeddings,
        index_name=index_name,
        documents=chunks,
        namespace=user_id,
    )
    return vectordb
