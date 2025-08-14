from fastapi import HTTPException, status
from typing import Any, Optional

class ValidationException(HTTPException):
    """Custom exception for validation errors."""
    
    def __init__(self, detail: Any = None, code: Optional[int] = status.HTTP_422_UNPROCESSABLE_ENTITY):
        super().__init__(status_code=code, detail=detail or "Validation error occurred.")


class BusinessException(HTTPException):
    """Custom exception for business logic errors."""
    
    def __init__(self, detail: Any = None, code: Optional[int] = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=code, detail=detail or "Business logic error occurred.")
