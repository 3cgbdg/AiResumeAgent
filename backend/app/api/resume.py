from fastapi import APIRouter,UploadFile,File
import shutil
import tempfile
import os
import uuid
from ..rag.resume_loader import load_resume
from ..rag.vector_store import create_vector_store

router = APIRouter(prefix="/resume",tags=["resume"])

@router.post("/upload")
def upload_resume(file :UploadFile = File(...)):
    
    user_id = str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name
    
    docs = load_resume(file_path)
    create_vector_store(docs,user_id)
    
    os.remove(file_path)
    
    return {
        "message": "Resume uploaded and indexed",
        "user_id": user_id
    }
