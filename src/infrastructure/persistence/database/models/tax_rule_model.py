from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, Numeric, JSON, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from .base_model import BaseModel
import uuid

class TaxRuleModel(BaseModel):
    __tablename__ = "tax_rules"

    rule_type = Column(String(50), nullable=False, index=True)  # e.g., 'income_tax', 'sales_tax'
    version = Column(String(20), nullable=False)
    tax_date = Column(DateTime, nullable=False, index=True)  # When this rule becomes effective
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    tax_rule = Column(JSONB, nullable=False)  # The actual tax calculation rules
    rule_definition = Column(JSON, nullable=False) # The actual tax calculation rules
    
    
    def __repr__(self):
        return f"<TaxRule(rule_name='{self.rule_name}', version='{self.version}', country='{self.country_code}')>"