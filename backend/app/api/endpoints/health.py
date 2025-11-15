from fastapi import APIRouter, Depends
import time
import psutil
import os

from app.core.schemas import HealthResponse
from app.models.model_loader import model_loader

router = APIRouter()

start_time = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        model_loaded=model_loader.models_loaded,
        version="1.0.0",
        uptime=round(uptime, 2)
    )

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with system information"""
    uptime = time.time() - start_time
    
    # Get system information
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime_seconds": round(uptime, 2),
        "model_loaded": model_loader.models_loaded,
        "system": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory": {
                "total": round(memory.total / (1024**3), 2),
                "available": round(memory.available / (1024**3), 2),
                "percent": memory.percent
            },
            "disk": {
                "total": round(disk.total / (1024**3), 2),
                "used": round(disk.used / (1024**3), 2),
                "free": round(disk.free / (1024**3), 2),
                "percent": round((disk.used / disk.total) * 100, 2)
            }
        },
        "model": {
            "type": "Custom Trained" if model_loader.use_custom_model else "Ensemble",
            "device": str(model_loader.device),
            "loaded": model_loader.models_loaded
        }
    }