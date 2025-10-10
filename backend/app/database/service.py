from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json
import hashlib
from app.database.models import AnalysisRecord, AuditLog
from app.core.schemas import AnalysisResult
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    """Service layer for database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_analysis_record(
        self,
        analysis_result: AnalysisResult,
        image_info: Dict[str, Any],
        session_info: Dict[str, Any]
    ) -> AnalysisRecord:
        """Create a new analysis record in the database"""
        
        # Create analysis record
        record = AnalysisRecord(
            image_filename=image_info.get('filename', 'unknown'),
            image_size=image_info.get('size'),
            image_width=image_info.get('width'),
            image_height=image_info.get('height'),
            dr_stage=analysis_result.stage.value,
            confidence_score=analysis_result.confidence,
            risk_level=analysis_result.risk_level.value,
            processing_time=analysis_result.processing_time,
            stage_description=analysis_result.stage_description,
            recommendations=json.dumps(analysis_result.recommendations),
            session_id=session_info.get('session_id'),
            ip_hash=self._hash_ip(session_info.get('ip_address', '')),
            model_type=session_info.get('model_type', 'resnet50')
        )
        
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        
        # Log the analysis event
        self.log_audit_event(
            event_type="analysis_completed",
            event_description=f"Analysis completed for stage {analysis_result.stage.value}",
            session_info=session_info,
            analysis_id=record.id
        )
        
        logger.info(f"Analysis record created: {record.id}")
        return record
    
    def get_analysis_record(self, record_id: str) -> Optional[AnalysisRecord]:
        """Retrieve an analysis record by ID"""
        return self.db.query(AnalysisRecord).filter(AnalysisRecord.id == record_id).first()
    
    def get_recent_analyses(
        self, 
        limit: int = 10, 
        session_id: Optional[str] = None
    ) -> List[AnalysisRecord]:
        """Get recent analysis records"""
        query = self.db.query(AnalysisRecord)
        
        if session_id:
            query = query.filter(AnalysisRecord.session_id == session_id)
        
        return query.order_by(desc(AnalysisRecord.created_at)).limit(limit).all()
    
    def get_analysis_statistics(self, days: int = 30) -> Dict[str, Any]:
        """Get analysis statistics for the last N days"""
        since_date = datetime.utcnow() - timedelta(days=days)
        
        records = self.db.query(AnalysisRecord).filter(
            AnalysisRecord.created_at >= since_date
        ).all()
        
        if not records:
            return {
                "total_analyses": 0,
                "stage_distribution": {},
                "average_confidence": 0,
                "average_processing_time": 0
            }
        
        # Calculate statistics
        total_analyses = len(records)
        stage_distribution = {}
        total_confidence = 0
        total_processing_time = 0
        
        for record in records:
            # Stage distribution
            stage = record.dr_stage
            stage_distribution[stage] = stage_distribution.get(stage, 0) + 1
            
            # Averages
            total_confidence += record.confidence_score
            if record.processing_time:
                total_processing_time += record.processing_time
        
        return {
            "total_analyses": total_analyses,
            "stage_distribution": stage_distribution,
            "average_confidence": round(total_confidence / total_analyses, 2),
            "average_processing_time": round(total_processing_time / total_analyses, 3),
            "period_days": days
        }
    
    def log_audit_event(
        self,
        event_type: str,
        event_description: str,
        session_info: Dict[str, Any],
        analysis_id: Optional[str] = None
    ) -> AuditLog:
        """Log an audit event for compliance"""
        
        audit_log = AuditLog(
            event_type=event_type,
            event_description=event_description,
            session_id=session_info.get('session_id'),
            ip_hash=self._hash_ip(session_info.get('ip_address', '')),
            user_agent_hash=self._hash_string(session_info.get('user_agent', '')),
            analysis_id=analysis_id
        )
        
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        
        return audit_log
    
    def get_audit_logs(
        self, 
        limit: int = 100,
        event_type: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> List[AuditLog]:
        """Get audit logs for compliance reporting"""
        query = self.db.query(AuditLog)
        
        if event_type:
            query = query.filter(AuditLog.event_type == event_type)
        
        if session_id:
            query = query.filter(AuditLog.session_id == session_id)
        
        return query.order_by(desc(AuditLog.timestamp)).limit(limit).all()
    
    def delete_old_records(self, days: int = 90) -> int:
        """Delete records older than specified days (for data retention compliance)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Delete old analysis records
        deleted_analyses = self.db.query(AnalysisRecord).filter(
            AnalysisRecord.created_at < cutoff_date
        ).delete()
        
        # Delete old audit logs
        deleted_logs = self.db.query(AuditLog).filter(
            AuditLog.timestamp < cutoff_date
        ).delete()
        
        self.db.commit()
        
        total_deleted = deleted_analyses + deleted_logs
        logger.info(f"Deleted {total_deleted} old records (analyses: {deleted_analyses}, logs: {deleted_logs})")
        
        return total_deleted
    
    def _hash_ip(self, ip_address: str) -> str:
        """Hash IP address for privacy compliance"""
        if not ip_address:
            return ""
        return hashlib.sha256(ip_address.encode()).hexdigest()[:16]
    
    def _hash_string(self, text: str) -> str:
        """Hash any string for privacy compliance"""
        if not text:
            return ""
        return hashlib.sha256(text.encode()).hexdigest()[:16]


def get_database_service(db: Session) -> DatabaseService:
    """Factory function to create database service"""
    return DatabaseService(db)