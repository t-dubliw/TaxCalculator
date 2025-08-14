"""
Main Application: FastAPI Tax Residency Rules Engine
Entry point for the tax residency calculation microservice.
"""
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any
from src.presentation.common.exception_handlers import business_exception_handler, generic_exception_handler, validation_exception_handler
from src.presentation.api.v1.controllers.tax_calculation_controller import router as tax_calc_router
from src.presentation.api.v1.controllers.health_controller import router as health_router

from src.infrastructure.configuration.app_settings import settings
from src.infrastructure.configuration.dependency_injection import setup_dependencies
from src.shared.exceptions.base_exceptions import ValidationException, BusinessException
from src.presentation.api.v1.schemas.common.base_response import ErrorResponse


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Tax Rules Engine...")
    
    # Initialize dependencies
    app.state.settings = settings
    await setup_dependencies(app)
    yield
    
    logger.info("Shutting down Tax Rules Engine...")

    logger.info("Tax Rules Engine shutdown complete")


app = FastAPI(
    title="Tax Rules Engine",
    description="""
    A microservice for determining tax rule and calculating tax amounts based on configurable, versioned tax rules.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom exception handlers
@app.exception_handler(ValidationException)
async def validation_exception_handler_wrapper(request: Request, exc: ValidationException):
    """Handle validation exceptions."""
    return await validation_exception_handler(request, exc)


@app.exception_handler(BusinessException)
async def business_exception_handler_wrapper(request: Request, exc: BusinessException):
    """Handle business exceptions."""
    return await business_exception_handler(request, exc)


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic validation errors."""
    logger.warning(f"Pydantic validation error: {exc}")
    
    # Extract field errors
    field_errors = {}
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"])
        field_errors[field] = error["msg"]
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            success=False,
            message="Request validation failed",
            error_code="VALIDATION_ERROR",
            details=f"Validation failed for {len(field_errors)} field(s)",
            field_errors=field_errors
        ).dict()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler_wrapper(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    # Convert HTTPException to our standard error response
    error_code_map = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        422: "UNPROCESSABLE_ENTITY",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_ERROR"
    }
    
    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message=exc.detail if isinstance(exc.detail, str) else "HTTP error occurred",
            error_code=error_code,
            details=str(exc.detail) if not isinstance(exc.detail, str) else None
        ).dict()
    )


@app.exception_handler(Exception)
async def generic_exception_handler_wrapper(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    return await generic_exception_handler(request, exc)


app.include_router(health_router, prefix="/api/v1")
app.include_router(tax_calc_router, prefix="/api/v1")



@app.get("/")
async def root():
    """Root endpoint with basic service information."""
    return {
        "service": "Tax Rule Engine",
        "version": "1.0.0",
        "description": "Microservice for tax calculation",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Set to False in production
        log_level="info"
    )