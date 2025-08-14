"""
API Schema: Tax Calculation Response
Pydantic models for tax calculation API responses.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class TaxCalculationResponse(BaseModel):
    income: float
    tax_amount: float
    rule_version: str
    breakdown: Optional[List[Dict[str, Any]]] = None