from fastapi import Request
from fastapi.responses import JSONResponse

import logging

from src.presentation.api.v1.schemas.common.base_response import ErrorResponse
from src.shared.exceptions.base_exceptions import BusinessException, ValidationException

logger = logging.getLogger(__name__)

# --- Custom exception handlers ---
async def validation_exception_handler(request: Request, exc: ValidationException):
    logger.warning(f"ValidationException: {exc}")
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            success=False,
            message=str(exc),
            error_code="VALIDATION_ERROR"
        ).dict()
    )

async def business_exception_handler(request: Request, exc: BusinessException):
    logger.warning(f"BusinessException: {exc}")
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            success=False,
            message=str(exc),
            error_code="BUSINESS_ERROR"
        ).dict()
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            message="Internal server error",
            error_code="INTERNAL_ERROR"
        ).dict()
    )
