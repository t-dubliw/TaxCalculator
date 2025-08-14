"""
API Schema: Tax Calculation Response
Pydantic models for tax calculation API responses.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# class DeterminationFactor(BaseModel):
#     """Individual factor that influenced the tax residency determination."""
#     factor: str = Field(..., description="Name of the determination factor")
#     value: str = Field(..., description="Value of the factor")
#     threshold: Optional[str] = Field(None, description="Threshold or requirement for this factor")
#     impact: str = Field(..., description="Impact on determination (positive, negative, neutral)")
#     weight: Optional[float] = Field(None, description="Weight of this factor in the decision")


# class RuleApplication(BaseModel):
#     """Details of how a specific rule was applied."""
#     rule_type: str = Field(..., description="Type of rule applied")
#     rule_version: str = Field(..., description="Version of the rule")
#     applied_rule: Dict[str, Any] = Field(..., description="The specific rule configuration applied")
#     user_value: Any = Field(..., description="User's value for this rule")
#     result: str = Field(..., description="Result of applying this rule")


# class CalculationData(BaseModel):
#     """Core calculation result data."""
#     calculation_id: str = Field(..., description="Unique identifier for this calculation")
#     tax_year: int = Field(..., description="Tax year for the calculation")
#     country_code: str = Field(..., description="Country code for tax calculation")
#     rule_version: str = Field(..., description="Version of tax rules used")
#     residency_status: str = Field(..., description="Determined tax residency status")
#     is_tax_resident: bool = Field(..., description="Whether individual is considered a tax resident")
#     calculated_tax: float = Field(..., description="Calculated tax amount")
#     tax_rate_percentage: float = Field(..., description="Applied tax rate as percentage")
#     explanation: str = Field(..., description="Human-readable explanation of the calculation")
#     determination_factors: List[DeterminationFactor] = Field(
#         ..., 
#         description="Factors that influenced the residency determination"
#     )
#     rule_applications: List[RuleApplication] = Field(
#         ..., 
#         description="Details of how specific rules were applied"
#     )
#     calculated_at: str = Field(..., description="Timestamp when calculation was performed")
#     calculation_duration_ms: Optional[int] = Field(
#         None, 
#         description="Time taken to perform the calculation in milliseconds"
#     )


# class TaxCalculationResponse(BaseModel):
#     """Response model for successful tax calculation."""
#     success: bool = Field(True, description="Whether the operation was successful")
#     message: str = Field(..., description="Response message")
#     data: CalculationData = Field(..., description="Calculation result data")
#     timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
#     class Config:
#         """Pydantic model configuration."""
#         schema_extra = {
#             "example": {
#                 "success": True,
#                 "message": "Tax calculation completed successfully",
#                 "data": {
#                     "calculation_id": "calc_123456789",
#                     "tax_year": 2024,
#                     "country_code": "US",
#                     "rule_version": "1.2.0",
#                     "residency_status": "tax_resident",
#                     "is_tax_resident": True,
#                     "calculated_tax": 11250.00,
#                     "tax_rate_percentage": 15.00,
#                     "explanation": "Tax residency status: tax_resident\nApplied tax rate: 15.00%\nCalculated tax amount: $11,250.00\n\nKey determination factors:\n• physical_presence: 200 days in country (impact: positive)\n• permanent_home: Yes (impact: positive)",
#                     "determination_factors": [
#                         {
#                             "factor": "physical_presence",
#                             "value": "200 days in country",
#                             "threshold": "183 days required",
#                             "impact": "positive",
#                             "weight": 0.6
#                         }
#                     ],
#                     "rule_applications": [
#                         {
#                             "rule_type": "income_bracket",
#                             "rule_version": "1.2.0",
#                             "applied_rule": {
#                                 "min_income": 50000,
#                                 "max_income": 100000,
#                                 "base_tax_rate": 0.15
#                             },
#                             "user_value": 75000.00,
#                             "result": "Applied 15.0% tax rate"
#                         }
#                     ],
#                     "calculated_at": "2024-01-15T10:30:00Z",
#                     "calculation_duration_ms": 45
#                 },
#                 "timestamp": "2024-01-15T10:30:00Z"
#             }
#         }


# class CalculationHistoryItem(BaseModel):
#     """Individual item in calculation history."""
#     calculation_id: str = Field(..., description="Unique identifier for the calculation")
#     user_id: str = Field(..., description="User who performed the calculation")
#     country_code: str = Field(..., description="Country for the calculation")
#     timestamp: str = Field(..., description="When the calculation was performed")
#     success: bool = Field(..., description="Whether the calculation was successful")
#     processing_time_ms: Optional[int] = Field(None, description="Processing time in milliseconds")
#     rule_version: Optional[str] = Field(None, description="Rule version used")
#     request_summary: Optional[Dict[str, Any]] = Field(None, description="Summary of request data")
#     result_summary: Optional[Dict[str, Any]] = Field(None, description="Summary of results")
#     error_message: Optional[str] = Field(None, description="Error message if calculation failed")


# class PaginationInfo(BaseModel):
#     """Pagination information for list responses."""
#     total: int = Field(..., description="Total number of records")
#     limit: int = Field(..., description="Maximum records per page")
#     offset: int = Field(..., description="Number of records skipped")
#     has_more: bool = Field(..., description="Whether there are more records available")


# class CalculationHistoryData(BaseModel):
#     """Data for calculation history response."""
#     calculations: List[CalculationHistoryItem] = Field(..., description="List of calculations")
#     pagination: PaginationInfo = Field(..., description="Pagination information")


# class CalculationHistoryResponse(BaseModel):
#     """Response model for calculation history."""
#     success: bool = Field(True, description="Whether the operation was successful")
#     message: str = Field(..., description="Response message")
#     data: CalculationHistoryData = Field(..., description="History data")
#     timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# class RuleVersionInfo(BaseModel):
#     """Information about a tax rule version."""
#     version: str = Field(..., description="Version number")
#     effective_from: str = Field(..., description="Date when version becomes effective")
#     effective_to: Optional[str] = Field(None, description="Date when version expires")
#     status: str = Field(..., description="Current status of the version")
#     rule_name: str = Field(..., description="Name/description of the rule")
#     is_current: bool = Field(..., description="Whether this is the current active version")


# class RuleVersionsData(BaseModel):
#     """Data for rule versions response."""
#     country_code: str = Field(..., description="Country code")
#     available_versions: List[RuleVersionInfo] = Field(..., description="Available rule versions")
#     total_versions: int = Field(..., description="Total number of versions")


# class RuleVersionsResponse(BaseModel):
#     """Response model for available rule versions."""
#     success: bool = Field(True, description="Whether the operation was successful")
#     message: str = Field(..., description="Response message")
#     data: RuleVersionsData = Field(..., description="Rule versions data")
#     timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# class ValidationResult(BaseModel):
#     """Validation result data."""
#     valid: bool = Field(..., description="Whether the request is valid")
#     errors: List[str] = Field(..., description="List of validation errors")
#     warnings: List[str] = Field(..., description="List of validation warnings")


# class ValidationResponse(BaseModel):
    # """Response model for request validation."""
    # success: bool = Field(True, description="Whether the validation completed successfully")
    # message: str = Field(..., description="Response message")
    # data: ValidationResult = Field(..., description="Validation results")
    # timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # class Config:
    #     """Pydantic model configuration."""
    #     schema_extra = {
    #         "example": {
    #             "success": True,
    #             "message": "Validation completed",
    #             "data": {
    #                 "valid": True,
    #                 "errors": [],
    #                 "warnings": ["Tax year 2024 is in the future"]
    #             },
    #             "timestamp": "2024-01-15T10:30:00Z"
    #         }
    #     }


class TaxCalculationResponse(BaseModel):
    income: float
    tax_amount: float
    rule_version: str
    breakdown: Optional[List[Dict[str, Any]]] = None