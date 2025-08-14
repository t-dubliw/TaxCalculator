# src/application/mappers/tax_rule_mapper.py
from typing import Dict, Any
from src.domain.entities.tax_rule import TaxRule
from src.presentation.api.v1.schemas.response.tax_calculation_response import TaxCalculationResponse

class TaxRuleMapper:
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> TaxRule:
        """Map dict from repository to domain entity."""
        return TaxRule(
            id=data["id"],
            rule_type=data["rule_type"],
            version=data["version"],
            tax_rule=data["tax_rule"],
            is_active=data["is_active"]
        )

    @staticmethod
    def to_tax_calculation_response(
        amount: float,
        result: Dict[str, Any],
        rule_version: str
    ) -> TaxCalculationResponse:
        """Map calculation result to API response."""
        return TaxCalculationResponse(
            income=amount,
            tax_amount=result["tax_amount"],
            rule_version=rule_version,
            breakdown=result.get("breakdown", {})
        )
