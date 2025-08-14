"""
Value Object: VersionNumber
Represents a semantic version number for tax rules.
"""
from dataclasses import dataclass
from typing import Tuple
import re


@dataclass(frozen=True)
class VersionNumber:
    """
    Immutable value object representing a semantic version number.
    Follows semantic versioning pattern: MAJOR.MINOR.PATCH
    """
    major: int
    minor: int
    patch: int
    
    def __post_init__(self):
        """Validate version components."""
        if not all(isinstance(v, int) and v >= 0 for v in (self.major, self.minor, self.patch)):
            raise ValueError("Version components must be non-negative integers")
    
    @property
    def value(self) -> str:
        """Get string representation of version."""
        return f"{self.major}.{self.minor}.{self.patch}"
    
    @classmethod
    def from_string(cls, version_str: str) -> 'VersionNumber':
        """
        Create VersionNumber from string format "major.minor.patch".
        
        Args:
            version_str: Version string like "1.0.0" or "2.1.3"
            
        Returns:
            VersionNumber instance
            
        Raises:
            ValueError: If version string format is invalid
        """
        if not isinstance(version_str, str):
            raise ValueError("Version must be a string")
        
        # Match semantic version pattern
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version_str.strip())
        if not match:
            raise ValueError("Version must follow semantic versioning format: major.minor.patch")
        
        major, minor, patch = map(int, match.groups())
        return cls(major, minor, patch)
    
    @classmethod
    def initial(cls) -> 'VersionNumber':
        """Create initial version (1.0.0)."""
        return cls(1, 0, 0)
    
    def increment_major(self) -> 'VersionNumber':
        """Create new version with incremented major version."""
        return VersionNumber(self.major + 1, 0, 0)
    
    def increment_minor(self) -> 'VersionNumber':
        """Create new version with incremented minor version."""
        return VersionNumber(self.major, self.minor + 1, 0)
    
    def increment_patch(self) -> 'VersionNumber':
        """Create new version with incremented patch version."""
        return VersionNumber(self.major, self.minor, self.patch + 1)
    
    def is_greater_than(self, other: 'VersionNumber') -> bool:
        """Compare if this version is greater than another."""
        return self._as_tuple() > other._as_tuple()
    
    def is_compatible_with(self, other: 'VersionNumber') -> bool:
        """Check if versions are compatible (same major version)."""
        return self.major == other.major
    
    def _as_tuple(self) -> Tuple[int, int, int]:
        """Convert to tuple for comparison."""
        return (self.major, self.minor, self.patch)
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, VersionNumber):
            return self._as_tuple() == other._as_tuple()
        return False
    
    def __lt__(self, other: 'VersionNumber') -> bool:
        return self._as_tuple() < other._as_tuple()
    
    def __hash__(self) -> int:
        return hash(self._as_tuple())