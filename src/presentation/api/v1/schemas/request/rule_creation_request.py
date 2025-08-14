from datetime import datetime
from typing import Any, Dict
from pydantic import Field
from pydantic_settings import BaseSettings


class TaxRuleCreateRequest(BaseSettings):
    rule_type: str = Field(..., description="Type of tax rule (e.g., 'income_tax')")
    version: str = Field(..., description="Rule version")
    tax_date: datetime = Field(..., description="Date when this rule becomes effective")
    tax_rule: Dict[str, Any] = Field(..., description="The tax calculation rules")
    is_active: bool = Field(default=True, description="Is this rule active")