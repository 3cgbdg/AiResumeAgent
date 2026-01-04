from fastapi import FastAPI
from .api.health import router as health_router
from .api.resume import router as resume_router
app = FastAPI(title="AI Resume Agent")

app.include_router(health_router)
app.include_router(resume_router)



