from langchain_community.document_loaders import PyPDFLoader

# loading pdf using its path 
def load_resume(path:str):
    loader = PyPDFLoader(path)
    docs = loader.load()
    return docs