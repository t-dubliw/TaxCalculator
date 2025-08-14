"""
Application Service: TaxCalculationService
Orchestrates tax calculation use cases and coordinates between domain and infrastructure.
"""
import uuid
from datetime import date
from typing import List, Optional, Dict, Any

from src.application.mappers.tax_rule_mapper import TaxRuleMapper
from src.application.services.SalesTaxCalculator import SalesTaxCalculator
from src.application.services.income_tax_calculator import IncomeTaxCalculator
from src.presentation.api.v1.schemas.response.tax_calculation_response import TaxCalculationResponse
from src.domain.entities.tax_rule import TaxRule


from ...domain.value_objects.country_code import CountryCode
from ...domain.value_objects.version_number import VersionNumber
from ...shared.exceptions.base_exceptions import BusinessException, ValidationException


class TaxCalculationService:
    """
    Application service for tax calculation operations.
    Coordinates between presentation layer, domain logic, and infrastructure.
    """
    
    def __init__(
        self,
        tax_rule_repository
    ):
        """
        Initialize the service with required dependencies.
        
        Args:
            tax_rule_repository: Repository for tax rule persistence
            audit_repository: Repository for audit record persistence
            mapper: Mapper for DTO transformations
        """
        self.tax_rule_repository = tax_rule_repository
        # self.audit_repository = audit_repository
        self.calculators = {
            "income_tax": IncomeTaxCalculator(),
            "sales_tax": SalesTaxCalculator()
        }
    

    async def calculate_tax(
        self,
        amount: float,
        rule_type: str
    ) -> TaxCalculationResponse:
        try:
            tax_data = self.tax_rule_repository.get_active_tax_rule(rule_type)

            if not tax_data or not tax_data.get("tax_rule"):
                raise BusinessException(f"No applicable tax rule found for {rule_type}")

            result = self.calculate_tax_by_rule_type(amount, rule_type, tax_data["tax_rule"])
            return TaxRuleMapper.to_tax_calculation_response(amount, result, tax_data["version"])

        except (ValidationException, BusinessException):
            raise
        except Exception as e:
            raise BusinessException(f"Tax calculation failed: {str(e)}")

    async def get_active_tax_rule(self, tax_type: str) -> TaxRule:
        try:
            data = self.tax_rule_repository.get_active_tax_rule(tax_type)
            return TaxRuleMapper.from_dict(data)
        except Exception as e:
            raise BusinessException(f"Failed to retrieve rule versions: {str(e)}")

    async def get_available_rules(self) -> List[TaxRule]:
        try:
            data_list = self.tax_rule_repository.get_all_versions()
            return [TaxRuleMapper.from_dict(d) for d in data_list]
        except Exception as e:
            raise BusinessException(f"Failed to retrieve rule versions: {str(e)}")

    async def create_tax_rule(
        self,
        rule_type: str,
        version: str,
        tax_date,
        tax_rule: Dict[str, Any],
        is_active: bool,
        created_by: str
    ) -> TaxRule:
        try:
            rule_data = {
                "rule_type": rule_type,
                "version": version,
                "tax_date": tax_date,
                "tax_rule": tax_rule,
                "rule_definition": tax_rule,
                "is_active": is_active,
                "created_by": created_by,
                "updated_by": created_by
            }
            created = self.tax_rule_repository.create_rule(rule_data)
            return TaxRuleMapper.from_dict(created)
        except (ValidationException, BusinessException):
            raise
        except Exception as e:
            raise BusinessException(f"Tax rule adding failed: {str(e)}")

    def calculate_tax_by_rule_type(self, amount: float, rule_type: str, rule_data: Dict[str, Any]):
        calculator = self.calculators.get(rule_type)
        if not calculator:
            raise BusinessException(f"Calculator not implemented for rule type '{rule_type}'")
        if not hasattr(calculator, "calculate"):
            raise BusinessException(f"Calculator for '{rule_type}' has no 'calculate' method")
        return calculator.calculate(amount, rule_data)
