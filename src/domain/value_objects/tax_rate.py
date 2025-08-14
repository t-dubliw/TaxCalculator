"""
Value Object: TaxRate
Represents a tax rate percentage with validation.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import Union


@dataclass(frozen=True)
class TaxRate:
    """
    Immutable value object representing a tax rate as a percentage.
    Stores rate as decimal (e.g., 0.15 for 15%).
    """
    rate: Decimal
    
    def __post_init__(self):
        """Validate tax rate."""
        if not isinstance(self.rate, Decimal):
            # Convert to Decimal if needed
            object.__setattr__(self, 'rate', Decimal(str(self.rate)))
        
        if self.rate < 0:
            raise ValueError("Tax rate cannot be negative")
        
        if self.rate > 1:
            raise ValueError("Tax rate cannot exceed 100% (1.0)")
    
    @classmethod
    def from_percentage(cls, percentage: Union[float, int, Decimal, str]) -> 'TaxRate':
        """
        Create TaxRate from percentage value.
        
        Args:
            percentage: Percentage value (e.g., 15 for 15%, 10.5 for 10.5%)
            
        Returns:
            TaxRate instance with decimal representation
        """
        decimal_rate = Decimal(str(percentage)) / Decimal('100')
        return cls(decimal_rate)
    
    @classmethod
    def from_decimal(cls, decimal_rate: Union[float, Decimal, str]) -> 'TaxRate':
        """
        Create TaxRate from decimal value.
        
        Args:
            decimal_rate: Decimal rate (e.g., 0.15 for 15%, 0.105 for 10.5%)
            
        Returns:
            TaxRate instance
        """
        return cls(Decimal(str(decimal_rate)))
    
    @classmethod
    def zero(cls) -> 'TaxRate':
        """Create zero tax rate."""
        return cls(Decimal('0'))
    
    def as_percentage(self) -> Decimal:
        """Get rate as percentage (e.g., 15.00 for 15%)."""
        return (self.rate * Decimal('100')).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
    
    def as_decimal(self) -> Decimal:
        """Get rate as decimal (e.g., 0.15 for 15%)."""
        return self.rate
    
    def calculate_tax(self, taxable_amount: Union[Decimal, float]) -> Decimal:
        """
        Calculate tax amount for given taxable amount.
        
        Args:
            taxable_amount: Amount to calculate tax on
            
        Returns:
            Tax amount as Decimal
        """
        amount = Decimal(str(taxable_amount))
        tax = amount * self.rate
        return tax.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def __str__(self) -> str:
        return f"{self.as_percentage()}%"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, TaxRate):
            return self.rate == other.rate
        return False
    
    def __hash__(self) -> int:
        return hash(self.rate)
    
    def __add__(self, other: 'TaxRate') -> 'TaxRate':
        """Add two tax rates."""
        return TaxRate(self.rate + other.rate)
    
    def __mul__(self, multiplier: Union[int, float, Decimal]) -> 'TaxRate':
        """Multiply tax rate by a number."""
        return TaxRate(self.rate * Decimal(str(multiplier)))