"""
API Schema: Base Response
Common response models and error handling schemas.
"""
from pydantic import BaseModel, Field
from typing import Any, Optional, Dict
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model for all API endpoints."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Timestamp when the response was generated"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class DataResponse(BaseResponse):
    """Base response model with data payload."""
    data: Any = Field(..., description="Response data")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": True,
                "message": "Data retrieved successfully",
                "data": {"key": "value"},
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ErrorResponse(BaseResponse):
    """Error response model."""
    success: bool = Field(False, description="Always false for error responses")
    error_code: str = Field(..., description="Specific error code for the error")
    details: Optional[str] = Field(None, description="Additional error details")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": "Annual income cannot be negative",
                "request_id": "req_123456789",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ValidationErrorResponse(ErrorResponse):
    """Validation error response with field-specific errors."""
    error_code: str = Field("VALIDATION_ERROR", description="Validation error code")
    field_errors: Optional[Dict[str, str]] = Field(
        None, 
        description="Field-specific validation errors"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Request validation failed",
                "error_code": "VALIDATION_ERROR",
                "details": "One or more fields failed validation",
                "field_errors": {
                    "annual_income": "Must be a positive number",
                    "days_in_country": "Must be between 0 and 366"
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class BusinessErrorResponse(ErrorResponse):
    """Business logic error response."""
    error_code: str = Field("BUSINESS_ERROR", description="Business error code")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Business rule violation",
                "error_code": "BUSINESS_ERROR",
                "details": "No applicable tax rule found for the specified country and year",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class NotFoundResponse(ErrorResponse):
    """Not found error response."""
    error_code: str = Field("NOT_FOUND", description="Resource not found error code")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Resource not found",
                "error_code": "NOT_FOUND",
                "details": "The requested calculation was not found",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class UnauthorizedResponse(ErrorResponse):
    """Unauthorized error response."""
    error_code: str = Field("UNAUTHORIZED", description="Authorization error code")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Unauthorized access",
                "error_code": "UNAUTHORIZED",
                "details": "Valid authentication token required",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class ForbiddenResponse(ErrorResponse):
    """Forbidden error response."""
    error_code: str = Field("FORBIDDEN", description="Access forbidden error code")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Access forbidden",
                "error_code": "FORBIDDEN",
                "details": "Insufficient permissions to access this resource",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class RateLimitResponse(ErrorResponse):
    """Rate limit exceeded error response."""
    error_code: str = Field("RATE_LIMIT_EXCEEDED", description="Rate limit error code")
    retry_after: Optional[int] = Field(None, description="Seconds to wait before retrying")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Rate limit exceeded",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "details": "Too many requests. Please wait before trying again.",
                "retry_after": 60,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class InternalServerErrorResponse(ErrorResponse):
    """Internal server error response."""
    error_code: str = Field("INTERNAL_ERROR", description="Internal server error code")
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": False,
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR",
                "details": "An unexpected error occurred. Please contact support.",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class HealthCheckResponse(BaseResponse):
    """Health check response model."""
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="Service version")
    uptime: Optional[int] = Field(None, description="Service uptime in seconds")
    dependencies: Optional[Dict[str, str]] = Field(
        None, 
        description="Status of service dependencies"
    )
    
    class Config:
        """Pydantic model configuration."""
        schema_extra = {
            "example": {
                "success": True,
                "message": "Service is healthy",
                "status": "healthy",
                "version": "1.0.0",
                "uptime": 3600,
                "dependencies": {
                    "database": "healthy",
                    "cache": "healthy"
                },
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }