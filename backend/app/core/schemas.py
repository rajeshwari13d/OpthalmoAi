from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    HIGH = "High"

class DiabeticRetinopathyStage(int, Enum):
    NO_DR = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    PROLIFERATIVE = 4

class ImageUploadResponse(BaseModel):
    message: str
    file_id: str
    file_name: str

class AnalysisResult(BaseModel):
    stage: DiabeticRetinopathyStage = Field(..., description="Diabetic retinopathy stage (0-4)")
    stage_description: str = Field(..., description="Human-readable stage description")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Confidence percentage")
    risk_level: RiskLevel = Field(..., description="Risk level assessment")
    recommendations: List[str] = Field(..., description="Clinical recommendations")
    processing_time: float = Field(..., description="Processing time in seconds")

class AnalysisResponse(BaseModel):
    success: bool
    result: Optional[AnalysisResult] = None
    error: Optional[str] = None
    medical_disclaimer: str
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
    uptime: float