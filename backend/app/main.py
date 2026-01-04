from fastapi import FastAPI
from backend.app.api.health import router as health_router
app = FastAPI(title="AI Resume Agent")

app.include_router()



