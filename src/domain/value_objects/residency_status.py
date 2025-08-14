"""
Value Object: ResidencyStatus
Represents the tax residency status of an individual.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ResidencyType(Enum):
    """Enumeration of possible residency statuses."""
    TAX_RESIDENT = "tax_resident"
    NON_RESIDENT = "non_resident"
    PARTIAL_RESIDENT = "partial_resident"
    DUAL_RESIDENT = "dual_resident"
    TEMPORARY_RESIDENT = "temporary_resident"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ResidencyStatus:
    """
    Immutable value object representing tax residency status.
    Includes the status type and optional additional context.
    """
    status_type: ResidencyType
    description: Optional[str] = None
    confidence_score: Optional[float] = None  # 0.0 to 1.0
    
    def __post_init__(self):
        """Validate residency status."""
        if not isinstance(self.status_type, ResidencyType):
            raise ValueError("status_type must be a ResidencyType enum")
        
        if self.confidence_score is not None:
            if not 0.0 <= self.confidence_score <= 1.0:
                raise ValueError("confidence_score must be between 0.0 and 1.0")
    
    @classmethod
    def temporary_resident(cls, description: Optional[str] = None, confidence: float = 1.0) -> 'ResidencyStatus':
        """Create a temporary resident status."""
        return cls(
            status_type=ResidencyType.TEMPORARY_RESIDENT,
            description=description or "Individual has temporary tax residency",
            confidence_score=confidence
        )
    
    @classmethod
    def unknown(cls, description: Optional[str] = None, confidence: float = 0.0) -> 'ResidencyStatus':
        """Create an unknown status."""
        return cls(
            status_type=ResidencyType.UNKNOWN,
            description=description or "Tax residency status could not be determined",
            confidence_score=confidence
        )
    
    def is_resident(self) -> bool:
        """Check if this status indicates any form of tax residency."""
        return self.status_type in {
            ResidencyType.TAX_RESIDENT,
            ResidencyType.PARTIAL_RESIDENT,
            ResidencyType.DUAL_RESIDENT,
            ResidencyType.TEMPORARY_RESIDENT
        }
    
    def is_full_resident(self) -> bool:
        """Check if this status indicates full tax residency."""
        return self.status_type == ResidencyType.TAX_RESIDENT
    
    def is_non_resident(self) -> bool:
        """Check if this status indicates non-residency."""
        return self.status_type == ResidencyType.NON_RESIDENT
    
    def is_uncertain(self) -> bool:
        """Check if residency status is uncertain."""
        return (self.status_type == ResidencyType.UNKNOWN or
                (self.confidence_score is not None and self.confidence_score < 0.7))
    
    @property
    def value(self) -> str:
        """Get string representation of status type."""
        return self.status_type.value
    
    def __str__(self) -> str:
        if self.confidence_score is not None:
            return f"{self.status_type.value} (confidence: {self.confidence_score:.1%})"
        return self.status_type.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, ResidencyStatus):
            return (self.status_type == other.status_type and
                    self.description == other.description and
                    self.confidence_score == other.confidence_score)
        return False
    
    def __hash__(self) -> int:
        return hash((self.status_type, self.description, self.confidence_score))
    def tax_resident(cls, description: Optional[str] = None, confidence: float = 1.0) -> 'ResidencyStatus':
        """Create a tax resident status."""
        return cls(
            status_type=ResidencyType.TAX_RESIDENT,
            description=description or "Individual is considered a tax resident",
            confidence_score=confidence
        )
    
    @classmethod
    def non_resident(cls, description: Optional[str] = None, confidence: float = 1.0) -> 'ResidencyStatus':
        """Create a non-resident status."""
        return cls(
            status_type=ResidencyType.NON_RESIDENT,
            description=description or "Individual is not considered a tax resident",
            confidence_score=confidence
        )
    
    @classmethod
    def partial_resident(cls, description: Optional[str] = None, confidence: float = 1.0) -> 'ResidencyStatus':
        """Create a partial resident status."""
        return cls(
            status_type=ResidencyType.PARTIAL_RESIDENT,
            description=description or "Individual has partial tax residency",
            confidence_score=confidence
        )
    
    @classmethod
    def dual_resident(cls, description: Optional[str] = None, confidence: float = 1.0) -> 'ResidencyStatus':
        """Create a dual resident status."""
        return cls(
            status_type=ResidencyType.DUAL_RESIDENT,
            description=description or "Individual is a dual tax resident",
            confidence_score=confidence
        )