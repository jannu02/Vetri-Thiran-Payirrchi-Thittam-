from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.routes import router

app = FastAPI(
    title=settings.app_title,
    description="AI-powered legal document generation API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", tags=["system"])
def root():
    return {
        "name": settings.app_title,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["system"])
def health():
    return {"status": "healthy"}
