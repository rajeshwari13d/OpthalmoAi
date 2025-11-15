"""
Simple Backend Test Server for OpthalmoAI
Minimal FastAPI server to test frontend-backend communication
"""
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="OpthalmoAI Test Backend", version="1.0.0")

# CORS middleware with specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class HealthResponse(BaseModel):
    status: str
    message: str
    model_loaded: bool = True

class AnalysisResult(BaseModel):
    result: Dict[str, Any]
    medical_disclaimer: str

# Health check endpoint
@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        logger.info("Health check requested")
        return HealthResponse(
            status="healthy",
            message="OpthalmoAI Test Backend is running",
            model_loaded=True
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# Analysis endpoint
@app.post("/api/v1/analyze", response_model=AnalysisResult)
async def analyze_image(file: UploadFile = File(...)):
    """Analyze uploaded retinal image"""
    try:
        logger.info(f"Analysis requested for file: {file.filename}")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
            
        # Check file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type")
        
        # Read file content (for validation)
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"File validated: {len(content)} bytes")
        
        # Create analysis result in format frontend expects
        frontend_result = {
            "id": f"analysis_{hash(file.filename) % 10000:04d}",
            "stage": 2,  # DR stage (0-4)
            "confidence": 0.87,  # Confidence as decimal (0.87 = 87%)
            "riskLevel": "moderate",  # low, moderate, high
            "recommendations": [
                "Continue regular diabetic management",
                "Follow up ophthalmology examination in 6 months", 
                "Monitor blood glucose levels closely",
                "Consider lifestyle modifications"
            ],
            "timestamp": "2024-01-15T10:30:00Z"
        }
        
        logger.info("Analysis completed successfully")
        
        # Return in exact format frontend expects
        return {
            "result": frontend_result,
            "medical_disclaimer": "This is an AI screening tool and should not replace professional medical diagnosis. Please consult with healthcare professionals for proper medical advice."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    print("Starting OpthalmoAI Test Backend...")
    print("Server: http://localhost:8004")
    print("Health: http://localhost:8004/api/v1/health") 
    print("Analysis: http://localhost:8004/api/v1/analyze")
    print("CORS: Allowing localhost:3000, localhost:3001, 127.0.0.1:3000")
    print("File upload endpoint: POST /api/v1/analyze")
    print("=" * 60)
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8004, 
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)