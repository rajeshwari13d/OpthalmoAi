import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "OpthalmoAI"
    
    # Development Settings
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://opthalmoai.web.app",
        "https://opthalmoai.firebaseapp.com"
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".bmp"]
    UPLOAD_DIRECTORY: str = "uploads"
    
    # Model Settings
    MODEL_PATH: str = "app/models/diabetic_retinopathy_model.pth"
    MODEL_TYPE: str = "resnet50"  # or "vgg16"
    
    # Medical Compliance
    MEDICAL_DISCLAIMER: str = ("This is an assistive screening tool and is NOT a substitute "
                              "for professional medical diagnosis. Always consult with a "
                              "qualified healthcare professional.")
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./opthalmoai.db"
    
    # Data Retention (compliance)
    DATA_RETENTION_DAYS: int = 90  # Keep records for 90 days
    ENABLE_AUDIT_LOGGING: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables

settings = Settings()