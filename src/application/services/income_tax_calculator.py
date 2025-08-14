from typing import Any, Dict
from .base_calculator import BaseTaxCalculator

class IncomeTaxCalculator(BaseTaxCalculator):
    def calculate(self, amount: float, rule: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate income tax based on tax brackets"""
        brackets = rule.get("brackets", [])
        if not brackets:
            raise ValueError("No tax brackets defined in rule")
        
        total_tax = 0
        breakdown = []
        remaining_amount = amount
        
        for bracket in sorted(brackets, key=lambda x: x.get("min_amount", 0)):
            min_amount = bracket.get("min_amount", 0)
            max_amount = bracket.get("max_amount")
            rate = bracket.get("rate", 0) / 100  # Convert percentage to decimal
            
            if remaining_amount <= 0:
                break
                
            # Calculate taxable amount in this bracket
            if max_amount is None:  # Highest bracket
                taxable_in_bracket = remaining_amount
            else:
                taxable_in_bracket = min(remaining_amount, max_amount - min_amount)
            
            if amount > min_amount:
                actual_taxable = min(taxable_in_bracket, amount - min_amount)
                if actual_taxable > 0:
                    bracket_tax = actual_taxable * rate
                    total_tax += bracket_tax
                    
                    breakdown.append({
                        "bracket": f"{min_amount}-{max_amount if max_amount else 'above'}",
                        "rate": f"{rate*100:.2f}%",
                        "taxable_amount": f"{actual_taxable:.2f}",
                        "tax": f"{bracket_tax:.2f}"
                    })
                    
                    remaining_amount -= actual_taxable
        
        return {
            "tax_amount": round(total_tax, 2),
            "breakdown": breakdown
        }
