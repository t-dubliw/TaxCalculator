from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime

from src.domain.entities.tax_rule import TaxRule
from src.domain.value_objects.country_code import CountryCode
from src.domain.value_objects.version_number import VersionNumber




class TaxRuleRepositoryInterface(ABC):
    """Interface for tax rule repository"""

    @abstractmethod
    async def create_rule(self, rule_data: Dict[str, Any]) -> TaxRule:
        """Create a new tax rule"""
        pass

    @abstractmethod
    async def get_rule_by_id(self, rule_id: str) -> Optional[TaxRule]:
        """Get a tax rule by its ID"""
        pass

    @abstractmethod
    async def get_rule_by_version(
        self,
        rule_name: str,
        version: str,
        country_code: str
    ) -> Optional[TaxRule]:
        """Get a rule by name, version, and country code"""
        pass

    @abstractmethod
    async def get_active_rule(
        self,
        rule_name: str,
        country_code: str,
        tax_year: str,
        as_of_date: Optional[datetime] = None
    ) -> Optional[TaxRule]:
        """Get the active rule for a given date"""
        pass

    @abstractmethod
    async def get_latest_version(
        self,
        rule_name: str,
        country_code: str
    ) -> Optional[TaxRule]:
        """Get the latest version of a rule"""
        pass

    @abstractmethod
    async def get_all_versions(
        self
    ) -> List[TaxRule]:
        """Get all versions of a rule"""
        pass


