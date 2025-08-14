# src/infrastructure/configuration/dependency_injection.py
from fastapi import Depends, FastAPI, Request

from src.application.services.tax_calculation_service import TaxCalculationService
# from src.domain.repositories.tax_rule_repository_interface import TaxRuleRepositoryInterface
from src.infrastructure.persistence.database.config.connection_factory import connection_factory
from src.infrastructure.persistence.database.config.database_config import db_config
from src.infrastructure.persistence.database.repositories.tax_rule_repository_impl import TaxRuleRepositoryImpl


async def setup_dependencies(app: FastAPI):
    """
    Setup application dependencies (repositories, services, mappers)
    """
    # Initialize database tables
    db_config.create_tables()

    # Repository
    tax_rule_repo = TaxRuleRepositoryImpl(connection_factory=connection_factory)


    # Service
    tax_service = TaxCalculationService(
        tax_rule_repository=tax_rule_repo
    )

    # Attach to app state
    app.state.tax_rule_repository = tax_rule_repo
    app.state.tax_calculation_service = tax_service

    @app.on_event("shutdown")
    async def shutdown_event():
        db_config.drop_tables()


# Dependency function to get service from app.state
def get_tax_calculation_service(request: Request) -> TaxCalculationService:
    """FastAPI dependency function to inject TaxCalculationService."""
    return request.app.state.tax_calculation_service


# Dependency function to get controller
def get_tax_calculation_controller(
    service: TaxCalculationService = Depends(get_tax_calculation_service)
):
    from src.presentation.api.v1.controllers.tax_calculation_controller import TaxCalculationController
    """FastAPI dependency function to inject TaxCalculationController."""
    return TaxCalculationController(service)
