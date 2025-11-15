#!/usr/bin/env python3
"""
Simplified Backend Server for Testing
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import json
from typing import Dict, Any
import uvicorn

# Create FastAPI app
app = FastAPI(title="OpthalmoAI Test API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
    uptime: float

class AnalysisResponse(BaseModel):
    result: Dict[str, Any]
    medical_disclaimer: str

# Global variables
start_time = time.time()
model_loaded = False

@app.get("/")
async def root():
    return {
        "message": "OpthalmoAI Test API - Simplified Backend",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/api/v1/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        model_loaded=True,  # Simplified - always return True
        version="1.0.0",
        uptime=round(uptime, 2)
    )

@app.post("/api/v1/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """Simplified analysis endpoint for testing"""
    print(f"Analysis endpoint called with file: {file.filename if file else 'No file'}")
    
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
            
        print(f"File details: {file.filename} ({file.content_type}) - {file.size if hasattr(file, 'size') else 'size unknown'} bytes")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read the image
        image_data = await file.read()
        print(f"Successfully read image: {len(image_data)} bytes")
        
        # Simulate AI analysis (mock result)
        mock_result = {
            "id": f"analysis_{int(time.time())}",
            "stage": 2,  # Mock stage
            "stage_description": "Moderate Non-proliferative Diabetic Retinopathy",
            "confidence": 78.5,
            "risk_level": "moderate",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": [
                "Schedule eye exams every 3-6 months",
                "Maintain optimal blood glucose control", 
                "Consider consultation with retinal specialist",
                "Monitor for signs of progression"
            ],
            "processing_time": 0.1,
            "model_info": {
                "model_name": "Test Model (Simplified Backend)",
                "use_custom_model": False,
                "prediction_details": {
                    "predicted_class": 2,
                    "confidence": 78.5
                }
            }
        }
        
        medical_disclaimer = (
            "MEDICAL DISCLAIMER: This is an AI-assisted screening tool and should not be "
            "considered as a substitute for professional medical diagnosis. Please consult "
            "with a qualified ophthalmologist for proper medical evaluation and treatment recommendations."
        )
        
        print(f"Analysis completed successfully for {file.filename}")
        
        response_data = {
            "result": mock_result,
            "medical_disclaimer": medical_disclaimer
        }
        
        print(f"Returning response: {len(str(response_data))} characters")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
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
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server failed to start: {e}")
        import traceback
        traceback.print_exc()