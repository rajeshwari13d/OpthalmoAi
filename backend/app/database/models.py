from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from app.core.config import settings

Base = declarative_base()

class AnalysisRecord(Base):
    """Database model for storing analysis results"""
    __tablename__ = "analysis_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Image information (anonymized)
    image_filename = Column(String, nullable=False)  # Anonymized filename
    image_size = Column(Integer)  # File size in bytes
    image_width = Column(Integer)
    image_height = Column(Integer)
    
    # Analysis results
    dr_stage = Column(Integer, nullable=False)  # 0-4 diabetic retinopathy stage
    confidence_score = Column(Float, nullable=False)  # 0-100 confidence percentage
    risk_level = Column(String, nullable=False)  # low, moderate, high
    processing_time = Column(Float)  # Time taken for analysis in seconds
    
    # Clinical information
    stage_description = Column(Text)
    recommendations = Column(Text)  # JSON string of recommendations
    medical_disclaimer = Column(Text)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Privacy and compliance
    patient_id = Column(String)  # Optional anonymized patient ID
    session_id = Column(String)  # Session identifier
    ip_hash = Column(String)  # Hashed IP for audit purposes
    
    # Model information
    model_version = Column(String, default="1.0.0")
    model_type = Column(String, default="resnet50")
    
    def __repr__(self):
        return f"<AnalysisRecord(id={self.id}, stage={self.dr_stage}, confidence={self.confidence_score})>"


class AuditLog(Base):
    """Database model for audit logging (HIPAA compliance)"""
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Event information
    event_type = Column(String, nullable=False)  # upload, analysis, download, etc.
    event_description = Column(Text)
    
    # Session information
    session_id = Column(String)
    ip_hash = Column(String)  # Hashed IP
    user_agent_hash = Column(String)  # Hashed user agent
    
    # Analysis reference
    analysis_id = Column(String)  # Reference to analysis record
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, event={self.event_type})>"


# Database configuration
def get_database_url():
    """Get database URL from environment or default to SQLite"""
    return getattr(settings, 'DATABASE_URL', 'sqlite:///./opthalmoai.db')

# Create engine and session
engine = create_engine(
    get_database_url(),
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()