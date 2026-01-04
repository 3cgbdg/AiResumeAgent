from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pinecone
from pinecone import ServerlessSpec
from os import getenv

index_name = getenv("INDEX_NAME")

pc = pinecone.Pinecone(api_key=getenv("PINECONE_API_KEY"))

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
