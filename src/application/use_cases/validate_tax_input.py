from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any

class ValidationError(ValueError):
    pass

@dataclass
class ValidateTaxInputUseCase:
    def execute(self, payload: Dict[str, Any]) -> None:
        # MVP validation: days_in_country must be >= 0
        if "days_in_country" in payload and int(payload["days_in_country"]) < 0:
            raise ValidationError("days_in_country cannot be negative")
