"""
Value Object: CountryCode
Represents a standardized country code (ISO 3166-1 alpha-2).
"""
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CountryCode:
    """
    Immutable value object representing a country code.
    Uses ISO 3166-1 alpha-2 standard (e.g., 'US', 'UK', 'AU').
    """
    code: str
    
    def __post_init__(self):
        """Validate country code format."""
        if not isinstance(self.code, str):
            raise ValueError("Country code must be a string")
        
        if not re.match(r'^[A-Z]{2}$', self.code):
            raise ValueError("Country code must be exactly 2 uppercase letters (ISO 3166-1 alpha-2)")
    
    @classmethod
    def from_string(cls, code_str: str) -> 'CountryCode':
        """Create CountryCode from string, automatically converting to uppercase."""
        return cls(code_str.upper().strip())
    
    def __str__(self) -> str:
        return self.code
    
    def __eq__(self, other) -> bool:
        if isinstance(other, CountryCode):
            return self.code == other.code
        return False
    
    def __hash__(self) -> int:
        return hash(self.code)