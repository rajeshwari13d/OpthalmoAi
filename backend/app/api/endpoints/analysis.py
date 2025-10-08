from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import uuid
import time
from datetime import datetime
from typing import Dict, Any

from app.core.config import settings
from app.core.schemas import AnalysisResponse, ImageUploadResponse
from app.models.model_loader import model_loader
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    
    # Check file extension
    file_ext = os.path.splitext(file.filename or "")[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check content type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")

def anonymize_filename(original_filename: str) -> str:
    """Generate anonymous filename for privacy"""
    file_ext = os.path.splitext(original_filename)[1]
    unique_id = str(uuid.uuid4())
    timestamp = int(time.time())
    return f"img_{timestamp}_{unique_id[:8]}{file_ext}"

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_retinal_image(file: UploadFile = File(...)):
    """
    Analyze retinal fundus image for diabetic retinopathy detection
    """
    try:
        # Validate file
        validate_image(file)
        
        # Check file size
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
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
        if not model_loader.model_loaded:
            raise HTTPException(status_code=503, detail="Model not available")
        
        analysis_result = model_loader.predict(image)
        
        # Log analysis for monitoring (anonymized)
        logger.info(f"Analysis completed - Stage: {analysis_result.stage}, "
                   f"Confidence: {analysis_result.confidence}%, "
                   f"Processing time: {analysis_result.processing_time}s")
        
        return AnalysisResponse(
            success=True,
            result=analysis_result,
            error=None,
            medical_disclaimer=settings.MEDICAL_DISCLAIMER,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}")
        return AnalysisResponse(
            success=False,
            result=None,
            error="An unexpected error occurred during analysis",
            medical_disclaimer=settings.MEDICAL_DISCLAIMER,
            timestamp=datetime.now().isoformat()
        )

@router.post("/upload", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload and store retinal image (for batch processing or delayed analysis)
    """
    try:
        # Validate file
        validate_image(file)
        
        # Check file size
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Generate anonymous filename
        anonymous_filename = anonymize_filename(file.filename or "image.jpg")
        
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIRECTORY, anonymous_filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Generate file ID for tracking
        file_id = str(uuid.uuid4())
        
        logger.info(f"Image uploaded successfully - ID: {file_id}, Size: {len(contents)} bytes")
        
        return ImageUploadResponse(
            message="Image uploaded successfully",
            file_id=file_id,
            file_name=anonymous_filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

@router.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    return {
        "model_type": settings.MODEL_TYPE,
        "model_loaded": model_loader.model_loaded,
        "device": str(model_loader.device),
        "classes": [
            "No Diabetic Retinopathy (Stage 0)",
            "Mild Non-proliferative DR (Stage 1)", 
            "Moderate Non-proliferative DR (Stage 2)",
            "Severe Non-proliferative DR (Stage 3)",
            "Proliferative DR (Stage 4)"
        ],
        "input_size": "224x224 pixels",
        "supported_formats": settings.ALLOWED_EXTENSIONS,
        "max_file_size_mb": settings.MAX_FILE_SIZE // (1024*1024)
    }