from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc, func
from datetime import datetime, timezone

from ..models.audit_model import AuditModel
from ..config.connection_factory import connection_factory
import logging

logger = logging.getLogger(__name__)

class AuditRepositoryImpl:
    """Implementation of audit repository"""
    
    def __init__(self):
        self.connection_factory = connection_factory
    
    def create_audit_record(self, audit_data: Dict[str, Any]) -> AuditModel:
        """Create a new audit record"""
        with self.connection_factory.get_session() as session:
            audit_record = AuditModel(**audit_data)
            session.add(audit_record)
            session.flush()
            session.refresh(audit_record)
            return audit_record
    
    def get_audit_by_id(self, audit_id: str) -> Optional[AuditModel]:
        """Get audit record by ID"""
        with self.connection_factory.get_session() as session:
            return session.query(AuditModel).filter(
                AuditModel.audit_id == audit_id
            ).first()
    
    def get_user_audit_history(self, user_id: str, limit: int = 50, 
                              offset: int = 0) -> List[AuditModel]:
        """Get audit history for a specific user"""
        with self.connection_factory.get_session() as session:
            return session.query(AuditModel).filter(
                AuditModel.user_id == user_id
            ).order_by(desc(AuditModel.request_timestamp)).limit(limit).offset(offset).all()
    
    def get_audits_by_date_range(self, start_date: datetime, end_date: datetime,
                                user_id: Optional[str] = None) -> List[AuditModel]:
        """Get audit records within a date range"""
        with self.connection_factory.get_session() as session:
            query = session.query(AuditModel).filter(
                and_(
                    AuditModel.request_timestamp >= start_date,
                    AuditModel.request_timestamp <= end_date
                )
            )
            
            if user_id:
                query = query.filter(AuditModel.user_id == user_id)
            
            return query.order_by(desc(AuditModel.request_timestamp)).all()
    
    def get_audits_by_rule_version(self, rule_id: str, version: Optional[str] = None) -> List[AuditModel]:
        """Get audit records by rule ID and optionally version"""
        with self.connection_factory.get_session() as session:
            query = session.query(AuditModel).filter(
                AuditModel.rule_id_used == rule_id
            )
            
            if version:
                query = query.filter(AuditModel.rule_version_used == version)
            
            return query.order_by(desc(AuditModel.request_timestamp)).all()
    
    def get_audits_by_country_year(self, country_code: str, tax_year: str) -> List[AuditModel]:
        """Get audit records by country and tax year"""
        with self.connection_factory.get_session() as session:
            return session.query(AuditModel).filter(
                and_(
                    AuditModel.country_code == country_code,
                    AuditModel.tax_year == tax_year
                )
            ).order_by(desc(AuditModel.request_timestamp)).all()
    
    def get_calculation_stats(self, user_id: Optional[str] = None, 
                            country_code: Optional[str] = None,
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get calculation statistics"""
        with self.connection_factory.get_session() as session:
            query = session.query(AuditModel)
            
            # Apply filters
            filters = []
            if user_id:
                filters.append(AuditModel.user_id == user_id)
            if country_code:
                filters.append(AuditModel.country_code == country_code)
            if start_date:
                filters.append(AuditModel.request_timestamp >= start_date)
            if end_date:
                filters.append(AuditModel.request_timestamp <= end_date)
            
            if filters:
                query = query.filter(and_(*filters))
            
            # Calculate statistics
            total_calculations = query.count()
            
            if total_calculations == 0:
                return {
                    "total_calculations": 0,
                    "average_tax_amount": 0,
                    "total_tax_amount": 0,
                    "average_effective_rate": 0,
                    "unique_users": 0
                }
            
            stats = session.query(
                func.count(AuditModel.id).label('total'),
                func.avg(AuditModel.total_tax_amount).label('avg_tax'),
                func.sum(AuditModel.total_tax_amount).label('total_tax'),
                func.avg(AuditModel.effective_tax_rate).label('avg_rate'),
                func.count(func.distinct(AuditModel.user_id)).label('unique_users')
            ).filter(and_(*filters) if filters else True).first()
            
            return {
                "total_calculations": int(stats.total or 0),
                "average_tax_amount": float(stats.avg_tax or 0),
                "total_tax_amount": float(stats.total_tax or 0),
                "average_effective_rate": float(stats.avg_rate or 0),
                "unique_users": int(stats.unique_users or 0)
            }
    
    def search_audits(self, search_criteria: Dict[str, Any], 
                     limit: int = 100, offset: int = 0) -> List[AuditModel]:
        """Search audit records with flexible criteria"""
        with self.connection_factory.get_session() as session:
            query = session.query(AuditModel)
            
            # Build dynamic filter conditions
            filters = []
            
            if 'user_id' in search_criteria:
                filters.append(AuditModel.user_id == search_criteria['user_id'])
            
            if 'country_code' in search_criteria:
                filters.append(AuditModel.country_code == search_criteria['country_code'])
            
            if 'tax_year' in search_criteria:
                filters.append(AuditModel.tax_year == search_criteria['tax_year'])
            
            if 'rule_version' in search_criteria:
                filters.append(AuditModel.rule_version_used == search_criteria['rule_version'])
            
            if 'min_tax_amount' in search_criteria:
                filters.append(AuditModel.total_tax_amount >= search_criteria['min_tax_amount'])
            
            if 'max_tax_amount' in search_criteria:
                filters.append(AuditModel.total_tax_amount <= search_criteria['max_tax_amount'])
            
            if filters:
                query = query.filter(and_(*filters))
            
            return query.order_by(desc(AuditModel.request_timestamp)).limit(limit).offset(offset).all()