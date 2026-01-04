from fastapi import APIRouter
from ..core.llm import llm

router = APIRouter(prefix="/health")

@router.get('/')
async def health_check():
    response =  llm.invoke("Say ok if you work.")
    return {"llm_response": response}
