from typing import Any, Dict
from .base_calculator import BaseTaxCalculator


class SalesTaxCalculator(BaseTaxCalculator):
    def calculate(self, amount: float, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate sales tax based on a flat rate"""
        rate = rule.get("rate", 0) / 100
        tax_amount = round(amount * rate, 2)
        breakdown = [{"rate": f"{rate*100}%", "taxable_amount": amount, "tax": tax_amount}]

        return {
            "tax_amount": tax_amount,
            "breakdown": breakdown
        }
