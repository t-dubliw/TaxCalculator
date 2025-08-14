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
    
    # def create_rule(self, rule_data: Dict[str, Any]) -> TaxRuleModel:
    #     """Create a new tax rule"""
    #     with self.connection_factory.get_session() as session:
    #         rule = TaxRuleModel(**rule_data)
    #         session.add(rule)
    #         session.flush()
    #         session.refresh(rule)
    #         return rule
        
    # def create_rule(self, rule_data: Dict[str, Any]) -> Dict[str, Any]:
    #     with self.connection_factory.get_session() as session:
    #         rule = TaxRuleModel(**rule_data)
    #         session.add(rule)
    #         session.flush()
    #         session.refresh(rule)
    #         return {
    #             "id": rule.id,
    #             "rule_type": rule.rule_type,
    #             "version": rule.version,
    #             "tax_date": rule.tax_date,
    #             "tax_rule": rule.tax_rule,
    #             "is_active": rule.is_active,
    #             "created_at": rule.created_at,
    #             "updated_at": rule.updated_at,
    #         }
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


    def get_rule_by_id(self, rule_id: str) -> Optional[TaxRuleModel]:
        """Get rule by ID"""
        with self.connection_factory.get_session() as session:
            return session.query(TaxRuleModel).filter(
                TaxRuleModel.rule_id == rule_id
            ).first()
    
    def get_rule_by_version(self, rule_name: str, version: str, country_code: str) -> Optional[TaxRuleModel]:
        """Get rule by name, version, and country"""
        with self.connection_factory.get_session() as session:
            return session.query(TaxRuleModel).filter(
                and_(
                    TaxRuleModel.rule_name == rule_name,
                    TaxRuleModel.version == version,
                    TaxRuleModel.country_code == country_code
                )
            ).first()
    
    def get_active_rule(self, rule_name: str, country_code: str, tax_year: str, 
                       as_of_date: Optional[datetime] = None) -> Optional[TaxRuleModel]:
        """Get the active rule for a given date"""
        if as_of_date is None:
            as_of_date = datetime.now(timezone.utc)
        
        with self.connection_factory.get_session() as session:
            query = session.query(TaxRuleModel).filter(
                and_(
                    TaxRuleModel.rule_name == rule_name,
                    TaxRuleModel.country_code == country_code,
                    TaxRuleModel.tax_year == tax_year,
                    TaxRuleModel.is_active == True,
                    TaxRuleModel.effective_from <= as_of_date
                )
            )
            
            # Filter by effective_to if it exists
            query = query.filter(
                (TaxRuleModel.effective_to.is_(None)) |
                (TaxRuleModel.effective_to > as_of_date)
            )
            
            return query.order_by(desc(TaxRuleModel.effective_from)).first()
    
    def get_latest_version(self, rule_name: str, country_code: str) -> Optional[TaxRuleModel]:
        """Get the latest version of a rule"""
        with self.connection_factory.get_session() as session:
            return session.query(TaxRuleModel).filter(
                and_(
                    TaxRuleModel.rule_name == rule_name,
                    TaxRuleModel.country_code == country_code,
                    TaxRuleModel.is_active == True
                )
            ).order_by(desc(TaxRuleModel.created_at)).first()
    
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

    
    def get_rules_by_country(self, country_code: str, is_active: bool = True) -> List[TaxRuleModel]:
        """Get all rules for a specific country"""
        with self.connection_factory.get_session() as session:
            query = session.query(TaxRuleModel).filter(
                TaxRuleModel.country_code == country_code
            )
            
            if is_active:
                query = query.filter(TaxRuleModel.is_active == True)
            
            return query.order_by(
                TaxRuleModel.rule_name,
                desc(TaxRuleModel.created_at)
            ).all()
    
    def deactivate_rule(self, rule_id: str) -> bool:
        """Deactivate a rule"""
        with self.connection_factory.get_session() as session:
            rule = session.query(TaxRuleModel).filter(
                TaxRuleModel.rule_id == rule_id
            ).first()
            
            if rule:
                rule.is_active = False
                rule.effective_to = datetime.now(timezone.utc)
                return True
            return False
    
    def update_rule_metadata(self, rule_id: str, metadata_updates: Dict[str, Any]) -> bool:
        """Update rule metadata (description, etc.)"""
        with self.connection_factory.get_session() as session:
            rule = session.query(TaxRuleModel).filter(
                TaxRuleModel.rule_id == rule_id
            ).first()
            
            if rule:
                for key, value in metadata_updates.items():
                    if hasattr(rule, key) and key not in ['rule_id', 'id', 'created_at']:
                        setattr(rule, key, value)
                return True
            return False

