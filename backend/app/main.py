from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import health
from app.core.config import settings

app = FastAPI(
    title="OpthalmoAI API",
    description="AI-driven predictive ophthalmology platform for diabetic retinopathy screening",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
# app.include_router(prediction.router, prefix="/api/v1", tags=["prediction"])  # TODO: Enable after model setup

@app.get("/")
async def root():
    return {
        "message": "OpthalmoAI API - AI-driven predictive ophthalmology platform",
        "version": "1.0.0",
        "documentation": "/docs"
    }