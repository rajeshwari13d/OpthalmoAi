from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os
import uuid
import time
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.schemas import AnalysisResponse, ImageUploadResponse
from app.models.model_loader import model_loader
from app.database import get_db, get_database_service
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
async def analyze_retinal_image(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
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
        
        # Prepare session information
        session_info = {
            "session_id": str(uuid.uuid4()),  # Generate session ID
            "ip_address": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", ""),
            "model_type": settings.MODEL_TYPE
        }
        
        # Prepare image information
        image_info = {
            "filename": anonymize_filename(file.filename or "image.jpg"),
            "size": len(contents),
            "width": image.width,
            "height": image.height
        }
        
        # Save to database
        db_service = get_database_service(db)
        try:
            db_record = db_service.create_analysis_record(
                analysis_result=analysis_result,
                image_info=image_info,
                session_info=session_info
            )
            
            # Add record ID to response for potential future retrieval
            analysis_result_dict = {
                "id": db_record.id,
                "stage": analysis_result.stage,
                "stage_description": analysis_result.stage_description,
                "confidence": analysis_result.confidence,
                "risk_level": analysis_result.risk_level,
                "recommendations": analysis_result.recommendations,
                "processing_time": analysis_result.processing_time
            }
        
        except Exception as db_error:
            logger.error(f"Database save failed: {str(db_error)}")
            # Continue with analysis response even if DB save fails
            analysis_result_dict = {
                "id": str(uuid.uuid4()),  # Fallback ID
                "stage": analysis_result.stage,
                "stage_description": analysis_result.stage_description,
                "confidence": analysis_result.confidence,
                "risk_level": analysis_result.risk_level,
                "recommendations": analysis_result.recommendations,
                "processing_time": analysis_result.processing_time
            }
        
        # Log analysis for monitoring (anonymized)
        logger.info(f"Analysis completed - Stage: {analysis_result.stage}, "
                   f"Confidence: {analysis_result.confidence}%, "
                   f"Processing time: {analysis_result.processing_time}s")
        
        return AnalysisResponse(
            success=True,
            result=analysis_result_dict,
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

@router.get("/history")
async def get_analysis_history(
    limit: int = 10,
    session_id: str = None,
    db: Session = Depends(get_db)
):
    """Get analysis history (for authorized users only)"""
    try:
        db_service = get_database_service(db)
        records = db_service.get_recent_analyses(limit=limit, session_id=session_id)
        
        history = []
        for record in records:
            history.append({
                "id": record.id,
                "stage": record.dr_stage,
                "stage_description": record.stage_description,
                "confidence": record.confidence_score,
                "risk_level": record.risk_level,
                "created_at": record.created_at.isoformat(),
                "processing_time": record.processing_time,
                "image_size": f"{record.image_width}x{record.image_height}" if record.image_width else "unknown"
            })
        
        return {
            "success": True,
            "history": history,
            "count": len(history)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis history")

@router.get("/statistics")
async def get_analysis_statistics(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get analysis statistics for monitoring"""
    try:
        db_service = get_database_service(db)
        stats = db_service.get_analysis_statistics(days=days)
        
        return {
            "success": True,
            "statistics": stats
        }
        
    except Exception as e:
        logger.error(f"Error retrieving statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")