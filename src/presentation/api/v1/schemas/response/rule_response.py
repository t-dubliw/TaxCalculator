from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from src.presentation.api.v1.schemas.common.base_response import BaseResponse


class TaxRuleResponse(BaseSettings):
    id: int
    rule_type: str
    version: str
    is_active: bool
    tax_rule: Dict[str, Any]


class TaxRuleListResponse(BaseResponse):
    rules: List[TaxRuleResponse]
