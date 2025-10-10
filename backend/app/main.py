from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.endpoints import health, analysis
from app.core.config import settings
from app.models.model_loader import model_loader
from app.database import create_tables
import logging

# Setup logging
logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting OpthalmoAI API...")
    
    # Initialize database
    try:
        create_tables()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    # Load AI model
    try:
        model_loader.load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        logger.warning("API will run without model - analysis endpoint will return errors")
    
    yield
    
    # Shutdown
    logger.info("Shutting down OpthalmoAI API...")

app = FastAPI(
    title="OpthalmoAI API",
    description="AI-driven predictive ophthalmology platform for diabetic retinopathy screening",
    version="1.0.0",
    lifespan=lifespan
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
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])

@app.get("/")
async def root():
    return {
        "message": "OpthalmoAI API - AI-driven predictive ophthalmology platform",
        "version": "1.0.0",
        "documentation": "/docs"
    }