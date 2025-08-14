from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc
from datetime import datetime, timezone

from src.domain.repositories.tax_rule_repository_interface import TaxRuleRepositoryInterface

from ..models.tax_rule_model import TaxRuleModel
# from ..config.connection_factory import connection_factory
import logging

logger = logging.getLogger(__name__)

class TaxRuleRepositoryImpl():
    """Implementation of tax rule repository"""
    
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory
    
    def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        with self.connection_factory.get_session() as session:
            # 1️⃣ Mark previous rules of same type as inactive
            session.query(TaxRuleModel).filter(
                TaxRuleModel.rule_type == rule_data["rule_type"],
                TaxRuleModel.is_active == True
            ).update({"is_active": False}, synchronize_session=False)
    
            # 2️⃣ Create the new rule
            rule = TaxRuleModel(**rule_data)
            session.add(rule)
            session.flush()
            session.refresh(rule)
    
            return {
                "id": rule.id,
                "rule_type": rule.rule_type,
                "version": rule.version,
                "tax_date": rule.tax_date,
                "tax_rule": rule.tax_rule,
                "is_active": rule.is_active,
                "created_at": rule.created_at,
                "updated_at": rule.updated_at,
            }

    def get_all_versions(self) -> List[Dict[str, Any]]:
        """Get all versions of a rule as dictionaries"""
        with self.connection_factory.get_session() as session:
            rules = session.query(TaxRuleModel).order_by(desc(TaxRuleModel.created_at)).all()
            return [
                {
                    "id": r.id,
                    "rule_type": r.rule_type,
                    "version": r.version,
                    "tax_date": r.tax_date,
                    "tax_rule": r.tax_rule,
                    "is_active": r.is_active,
                    "created_at": r.created_at,
                    "updated_at": r.updated_at
                }
                for r in rules
            ]
        
    def get_active_tax_rule(self, rule_type) -> Dict[str, Any]:
        """Get all versions of a rule as dictionaries"""
        with self.connection_factory.get_session() as session:
            rule = session.query(TaxRuleModel).filter(
                TaxRuleModel.is_active == True,
                TaxRuleModel.rule_type == rule_type
            ).order_by(desc(TaxRuleModel.created_at)).first()
            if not rule:
                return None  # or raise exception if you prefer

            return {
                "id": rule.id,
                "rule_type": rule.rule_type,
                "version": rule.version,
                "tax_date": rule.tax_date,
                "tax_rule": rule.tax_rule,
                "is_active": rule.is_active,
                "created_at": rule.created_at,
                "updated_at": rule.updated_at
            }

