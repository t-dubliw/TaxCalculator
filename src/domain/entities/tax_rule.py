"""
Domain Entity: TaxRule
Represents an immutable tax residency rule with versioning support.
"""
from datetime import datetime, date
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from ..value_objects.country_code import CountryCode
from ..value_objects.version_number import VersionNumber
from ..value_objects.tax_rate import TaxRate


class RuleStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


@dataclass(frozen=True)
class TaxRule:
    """
    Immutable tax rule entity representing a specific version of tax residency rules.
    Each rule has a unique combination of country_code and version_number.
    """
    id: Optional[str]
    rule_type: str
    version: str
    tax_rule: Dict[str, Any]  # JSON structure containing the actual rules
    is_active: bool
