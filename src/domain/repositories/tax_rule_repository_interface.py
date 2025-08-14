"""
Domain Repository Interface: TaxRuleRepository
Repository interface for tax rule persistence operations.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import date

from ..entities.tax_rule import TaxRule
from ..value_objects.country_code import CountryCode
from ..value_objects.version_number import VersionNumber


class TaxRuleRepositoryInterface(ABC):
    """
    Abstract repository interface for tax rule persistence.
    Defines the contract for tax rule storage and retrieval operations.
    """
    
    @abstractmethod
    async def save(self, tax_rule: TaxRule) -> TaxRule:
        """
        Save a tax rule to the repository.
        
        Args:
            tax_rule: Tax rule to save
            
        Returns:
            Saved tax rule with generated ID if applicable
            
        Raises:
            RepositoryException: If save operation fails
        """
        pass
    
    @abstractmethod
    async def find_by_id(self, rule_id: str) -> Optional[TaxRule]:
        """
        Find a tax rule by its unique identifier.
        
        Args:
            rule_id: Unique identifier of the tax rule
            
        Returns:
            Tax rule if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_by_country_and_version(
        self, 
        country_code: CountryCode, 
        version: VersionNumber
    ) -> Optional[TaxRule]:
        """
        Find a tax rule by country code and version number.
        
        Args:
            country_code: Country code to search for
            version: Version number to search for
            
        Returns:
            Tax rule if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_active_rule_for_country(
        self, 
        country_code: CountryCode, 
        effective_date: Optional[date] = None
    ) -> Optional[TaxRule]:
        """
        Find the active tax rule for a country on a specific date.
        
        Args:
            country_code: Country code to search for
            effective_date: Date for which to find active rule (defaults to today)
            
        Returns:
            Active tax rule if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_latest_version_for_country(
        self, 
        country_code: CountryCode
    ) -> Optional[TaxRule]:
        """
        Find the latest version of tax rules for a country.
        
        Args:
            country_code: Country code to search for
            
        Returns:
            Latest tax rule version if found, None otherwise
        """
        pass
    
    @abstractmethod
    async def find_all_versions_for_country(
        self, 
        country_code: CountryCode
    ) -> List[TaxRule]:
        """
        Find all versions of tax rules for a country.
        
        Args:
            country_code: Country code to search for
            
        Returns:
            List of all tax rule versions for the country, ordered by version
        """
        pass
    
    @abstractmethod
    async def find_rules_by_effective_date_range(
        self, 
        start_date: date, 
        end_date: date,
        country_code: Optional[CountryCode] = None
    ) -> List[TaxRule]:
        """
        Find tax rules that were effective within a date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range
            country_code: Optional country filter
            
        Returns:
            List of tax rules effective within the date range
        """
        pass
    
    @abstractmethod
    async def exists(
        self, 
        country_code: CountryCode, 
        version: VersionNumber
    ) -> bool:
        """
        Check if a tax rule exists for a country and version.
        
        Args:
            country_code: Country code to check
            version: Version number to check
            
        Returns:
            True if rule exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def delete(self, rule_id: str) -> bool:
        """
        Delete a tax rule by ID.
        
        Args:
            rule_id: ID of rule to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_next_version_number(
        self, 
        country_code: CountryCode
    ) -> VersionNumber:
        """
        Get the next available version number for a country.
        
        Args:
            country_code: Country code to get next version for
            
        Returns:
            Next available version number
        """
        pass