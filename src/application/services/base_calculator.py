from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTaxCalculator(ABC):
    @abstractmethod
    def calculate(self, amount: float, rule_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate tax based on rule_data"""
        pass