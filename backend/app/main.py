from fastapi import FastAPI,Depends
from .api.resume import router as resume_router
from .api.chat import router as chat_router
from .core.rate_limit import rate_limit
app = FastAPI(title="AI Resume Agent")
from .core.llm import llm

# health endpoint
@app.get('/health')
async def health_check():
    response =  llm.invoke("Say ok if you work.")
    return {"llm_response": response}

app.include_router(resume_router,dependencies=[Depends(rate_limit)])
app.include_router(chat_router,dependencies=[Depends(rate_limit)])



