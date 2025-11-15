"""
Standalone FastAPI server for testing ResNet50 and VGG16 models
This script can be run from any directory
"""

import sys
import os
from pathlib import Path
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
import time
import uuid
from datetime import datetime

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

# Change working directory to backend
os.chdir(backend_dir)

# Now import the models
try:
    from app.models.model_loader import EnsembleModelLoader
    from app.core.schemas import DiabeticRetinopathyStage, RiskLevel
    print("✅ Successfully imported model components")
except Exception as e:
    print(f"❌ Failed to import models: {e}")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title="OpthalmoAI API",
    description="AI-powered diabetic retinopathy detection using ResNet50 and VGG16",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model loader
model_loader = None

@app.on_event("startup")
async def startup_event():
    """Load models on startup"""
    global model_loader
    try:
        print("🔄 Loading AI models...")
        model_loader = EnsembleModelLoader()
        model_loader.load_models()
        print("✅ Models loaded successfully!")
        print(f"   ResNet50: {'✓' if model_loader.resnet50_model else '✗'}")
        print(f"   VGG16: {'✓' if model_loader.vgg16_model else '✗'}")
        print(f"   Ensemble mode: {model_loader.ensemble_mode}")
    except Exception as e:
        print(f"❌ Failed to load models: {e}")
        model_loader = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpthalmoAI API - AI-powered diabetic retinopathy detection",
        "version": "1.0.0",
        "models_loaded": model_loader is not None and model_loader.models_loaded,
        "status": "ready" if model_loader and model_loader.models_loaded else "loading"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_loaded": model_loader is not None and model_loader.models_loaded,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/model-info")
async def get_model_info():
    """Get model information"""
    if not model_loader or not model_loader.models_loaded:
        raise HTTPException(status_code=503, detail="Models not loaded")
    
    return {
        "model_type": "ResNet50 + VGG16 Ensemble",
        "models_loaded": model_loader.models_loaded,
        "ensemble_mode": model_loader.ensemble_mode,
        "models": {
            "resnet50": model_loader.resnet50_model is not None,
            "vgg16": model_loader.vgg16_model is not None
        },
        "classes": [
            "No Diabetic Retinopathy (Stage 0)",
            "Mild Non-proliferative DR (Stage 1)", 
            "Moderate Non-proliferative DR (Stage 2)",
            "Severe Non-proliferative DR (Stage 3)",
            "Proliferative DR (Stage 4)"
        ],
        "input_size": "224x224 pixels",
        "supported_formats": [".jpg", ".jpeg", ".png", ".bmp"],
        "max_file_size_mb": 10
    }

def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    allowed_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    
    # Check file extension
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Check content type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

@app.post("/analyze")
async def analyze_retinal_image(file: UploadFile = File(...)):
    """
    Analyze retinal fundus image for diabetic retinopathy detection
    """
    try:
        # Check if models are loaded
        if not model_loader or not model_loader.models_loaded:
            raise HTTPException(status_code=503, detail="AI models not available")
        
        # Validate file
        validate_image(file)
        
        # Check file size (10MB limit)
        contents = await file.read()
        max_size = 10 * 1024 * 1024  # 10MB
        if len(contents) > max_size:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {max_size // (1024*1024)}MB"
            )
        
        # Load and validate image
        try:
            image = Image.open(io.BytesIO(contents))
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Check image dimensions (minimum requirements)
        if image.width < 224 or image.height < 224:
            raise HTTPException(
                status_code=400, 
                detail="Image too small. Minimum size: 224x224 pixels"
            )
        
        # Perform analysis
        start_time = time.time()
        analysis_result = model_loader.predict(image)
        processing_time = time.time() - start_time
        
        # Prepare response
        response = {
            "success": True,
            "result": {
                "id": str(uuid.uuid4()),
                "stage": int(analysis_result.stage),
                "stage_description": analysis_result.stage_description,
                "confidence": analysis_result.confidence,
                "risk_level": analysis_result.risk_level.value,
                "recommendations": analysis_result.recommendations,
                "processing_time": round(processing_time, 3),
                "model_info": getattr(analysis_result, 'model_info', None)
            },
            "medical_disclaimer": ("This is an assistive screening tool and is NOT a substitute "
                                  "for professional medical diagnosis. Always consult with a "
                                  "qualified healthcare professional."),
            "timestamp": datetime.now().isoformat()
        }
        
        # Log analysis
        print(f"📊 Analysis completed - Stage: {analysis_result.stage}, "
              f"Confidence: {analysis_result.confidence}%, "
              f"Processing time: {processing_time:.3f}s")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "An unexpected error occurred during analysis",
                "medical_disclaimer": ("This is an assistive screening tool and is NOT a substitute "
                                      "for professional medical diagnosis. Always consult with a "
                                      "qualified healthcare professional."),
                "timestamp": datetime.now().isoformat()
            }
        )

if __name__ == "__main__":
    print("🚀 Starting OpthalmoAI Standalone Server")
    print("📍 Backend directory:", backend_dir)
    print("🏥 Loading ResNet50 + VGG16 ensemble models...")
    
    # Run server
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8001,  # Use port 8001 instead of 8000
        reload=False,  # Disable reload for standalone mode
        log_level="info"
    )