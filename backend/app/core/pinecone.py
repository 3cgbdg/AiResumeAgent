from pinecone import Pinecone
from os import getenv
from dotenv import load_dotenv

load_dotenv()
# initializing pinecone client for correct env loading
def get_pinecone_client():
    api_key = getenv("PINECONE_API_KEY")
    if api_key is None:
        raise RuntimeError("Pinecone api_key is missing")
    return Pinecone(api_key=api_key)