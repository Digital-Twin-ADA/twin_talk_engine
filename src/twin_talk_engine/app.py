from fastapi import FastAPI

from twin_talk_engine.api import router as api_router

app = FastAPI(title="Twin Talk Engine API")

# Include API routes
app.include_router(api_router)
