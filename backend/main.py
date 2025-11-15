from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager

from app.api.endpoints import analysis, health
from app.core.config import settings
from app.models.model_loader import model_loader

# Initialize model loader
# model_loader is already imported as global instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the ML model
    model_loader.load_models()
    yield
    # Shutdown: Cleanup if needed
    pass

app = FastAPI(
    title="OpthalmoAI API",
    description="AI-driven predictive ophthalmology platform for diabetic retinopathy screening",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")

# Mount static files for uploaded images (with security considerations)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

@app.get("/")
async def root():
    return {"message": "OpthalmoAI API is running", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )