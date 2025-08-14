from typing import Optional
from pydantic import BaseModel, Field, validator

class TaxCalculationRequest(BaseModel):
    amount: float = Field(
        ..., 
        gt=0, 
        description="Amount to calculate tax for",
        example=1000.00
    )
    
    rule_type: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        description="Type of tax rule (e.g., 'income_tax')",
        example="income_tax"
    )

    @validator('rule_type')
    def validate_rule_type(cls, v):
        """Ensure rule_type contains only letters, underscores, or hyphens."""
        if not all(c.isalpha() or c in ['_'] for c in v):
            raise ValueError("rule_type must contain only letters, underscores")
        return v.lower()

    @validator('amount')
    def validate_amount(cls, v):
        """Ensure amount is positive and round to 2 decimals."""
        if v <= 0:
            raise ValueError("Amount must be greater than 0")
        return round(v, 2)
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 1000.00,
                "rule_type": "income_tax"
            }
        }
