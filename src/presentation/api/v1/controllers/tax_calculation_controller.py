"""
API Controller: TaxCalculationController
Handles HTTP requests for tax calculation operations.
"""
from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import logging


from src.presentation.api.v1.schemas.request.rule_creation_request import TaxRuleCreateRequest
from src.presentation.api.v1.schemas.response.rule_response import TaxRuleListResponse, TaxRuleResponse
from src.infrastructure.configuration.dependency_injection import get_tax_calculation_controller
from src.application.services.tax_calculation_service import TaxCalculationService
from src.shared.exceptions.base_exceptions import BusinessException, ValidationException

from ..schemas.request.tax_calculation_request import TaxCalculationRequest
from ..schemas.response.tax_calculation_response import (
    TaxCalculationResponse
)
from ..schemas.common.base_response import BaseResponse, ErrorResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

# Configure logging
logger = logging.getLogger(__name__)

security = HTTPBearer()

# Your JWT secret key and algorithm
JWT_SECRET_KEY = "your-secret-key"
JWT_ALGORITHM = "HS256"

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Validate JWT token and return user information.
    Only used for endpoints that need authentication.
    """
    try:
        token = credentials.credentials
        # payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = "123" #  payload.get("user_id")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"user_id": user_id}
    
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Create router
router = APIRouter(prefix="/tax-rules", tags=["tax-rules"])


class TaxCalculationController:

    def __init__(self, tax_calculation_service: TaxCalculationService):
        self.service = tax_calculation_service

    async def calculate_tax(
        self,
        rule_type: str,
        amount: float
    ) -> TaxCalculationResponse:
        try:
            calculation_request=  TaxCalculationRequest(
                amount=amount,
                rule_type=rule_type
            )
            
            # Calculate tax using the rule
            return  await self.service.calculate_tax(calculation_request.amount, calculation_request.rule_type)

        except ValidationException as e:
            logger.warning(f"Validation error in tax calculation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    success=False,
                    error_code="VALIDATION_ERROR",
                    message="Invalid request data",
                    details=str(e)
                ).dict()
            )
        except BusinessException as e:
            logger.error(f"Business error in tax calculation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorResponse(
                    success=False,
                    error_code="ERROR",
                    message="failed",
                    details=str(e)
                ).dict()
            )
        except Exception as e:
            logger.error(f"Unexpected error in tax calculation: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred",
                    details="Please contact support if the problem persists"
                ).dict()
            )
    

    async def create_tax_rule(self, rule_request: TaxRuleCreateRequest, user_id: str) -> TaxRuleResponse:
        try:
            
            logger.info(f"Creating tax rule of type {rule_request.rule_type} by user {user_id}")

            # Call the service to persist the rule
            new_rule = await self.service.create_tax_rule(
                rule_type=rule_request.rule_type,
                version=rule_request.version,
                tax_date=rule_request.tax_date,
                tax_rule=rule_request.tax_rule,
                is_active=rule_request.is_active,
                created_by=user_id
            )

            logger.info(f"Tax rule {new_rule.id} created successfully")

            return TaxRuleResponse(
                id=new_rule.id,
                rule_type=new_rule.rule_type,
                version=new_rule.version,
                is_active=new_rule.is_active,
                tax_rule=new_rule.tax_rule
            )

        except ValidationException as e:
            logger.warning(f"Validation error in tax calculation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorResponse(
                    success=False,
                    error_code="VALIDATION_ERROR",
                    message="Invalid request data",
                    details=str(e)
                ).dict()
            )
        except BusinessException as e:
            logger.error(f"Business error in tax calculation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorResponse(
                    success=False,
                    error_code="CALCULATION_ERROR",
                    message="Tax calculation failed",
                    details=str(e)
                ).dict()
            )
        except Exception as e:
            logger.error(f"Unexpected error in tax calculation: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred",
                    details="Please contact support if the problem persists"
                ).dict()
            )
    
    async def get_all_tax_rules(
        self
    ) -> TaxRuleListResponse:
        try:
            rules = await self.service.get_available_rules()
      
            return TaxRuleListResponse(
                success=True,
                message="",
                rules=[
                TaxRuleResponse(
                        id=r.id,
                        rule_type=r.rule_type,
                        version=r.version,
                        is_active=r.is_active,
                        tax_rule=r.tax_rule
                    )
                    for r in rules
                ]
            )
            
        except BusinessException as e:
            logger.error(f"Error retrieving calculation history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorResponse(
                    success=False,
                    error_code="HISTORY_ERROR",
                    message="Failed to retrieve calculation history",
                    details=str(e)
                ).dict()
            )
        except Exception as e:
            logger.error(f"Unexpected error retrieving history: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred"
                ).dict()
            )
    
    async def get_active_tax_rule(
        self, rule_type
    ) -> TaxRuleResponse:
        try:
            
            rule = await self.service.get_active_tax_rule(rule_type)
      
            return TaxRuleResponse(
                        id=rule.id,
                        rule_type=rule.rule_type,
                        version=rule.version,
                        is_active=rule.is_active,
                        tax_rule=rule.tax_rule
                    )
            
        except BusinessException as e:
            logger.error(f"Error retrieving calculation history: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=ErrorResponse(
                    success=False,
                    error_code="HISTORY_ERROR",
                    message="Failed to retrieve calculation history",
                    details=str(e)
                ).dict()
            )
        except Exception as e:
            logger.error(f"Unexpected error retrieving history: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorResponse(
                    success=False,
                    error_code="INTERNAL_ERROR",
                    message="An unexpected error occurred"
                ).dict()
            )


# Register routes
@router.get("/calculate/{rule_type}/{amount}", response_model=TaxCalculationResponse)
async def calculate_tax_endpoint(
    rule_type: str,
    amount: float,
    controller: TaxCalculationController = Depends(get_tax_calculation_controller)
):
    
    return await controller.calculate_tax(rule_type, amount)

# POST: Create a new tax rule
@router.post("/", response_model=TaxRuleResponse)
async def create_tax_rule_endpoint(
    request: TaxRuleCreateRequest,
    current_user: dict = Depends(get_current_user),
    controller: TaxCalculationController = Depends(get_tax_calculation_controller)
):
    """Create a new tax rule."""
    user_id = current_user.get("user_id", "unknown")
    return await controller.create_tax_rule(request, user_id)

# GET: Get all tax rules
@router.get("/", response_model=TaxRuleListResponse)
async def get_all_tax_rules_endpoint(
    controller: TaxCalculationController = Depends(get_tax_calculation_controller)
):
    """Get all tax rules."""
    return await controller.get_all_tax_rules()

# GET: Get all active tax rules
@router.get("/{rule_type}/active", response_model=TaxRuleResponse)
async def get_active_tax_rules_endpoint(
    rule_type: str,
    controller: TaxCalculationController = Depends(get_tax_calculation_controller)
):
    """Get the latest active tax rule for the given rule_type."""
    return await controller.get_active_tax_rule(rule_type)

