import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import HTTPException

from src.presentation.api.v1.controllers.tax_calculation_controller import TaxCalculationController, router
from src.application.services.tax_calculation_service import TaxCalculationService
from src.presentation.api.v1.schemas.response.tax_calculation_response import TaxCalculationResponse
from src.shared.exceptions.base_exceptions import BusinessException


class TestTaxCalculationAPI:
    
    @pytest.fixture
    def mock_tax_calculation_service(self):
        return Mock(spec=TaxCalculationService)
    
    @pytest.fixture
    def tax_controller(self, mock_tax_calculation_service):
        return TaxCalculationController(tax_calculation_service=mock_tax_calculation_service)
    
    @pytest.fixture
    def client(self, mock_tax_calculation_service):
        from fastapi import FastAPI
        app = FastAPI()
        app.include_router(router, prefix="/api/v1")
        
        # Mock the dependency
        def get_mock_controller():
            return TaxCalculationController(mock_tax_calculation_service)
        
        app.dependency_overrides[TaxCalculationController] = get_mock_controller
        
        return TestClient(app)
    
    @pytest.fixture
    def sample_calculation_response(self):
         return TaxCalculationResponse(
            income=50000.0,
            tax_amount=40000.0,
            rule_version="2024.1",
            breakdown=[{
                "bracket": "0-520.5",
                "rate": "10.00%",
                "taxable_amount": "122.00",
                "tax": "12.20"
            }]
        )
    
    @pytest.mark.asyncio
    async def test_calculate_tax_success(self, tax_controller, mock_tax_calculation_service, sample_calculation_response):
        """Test successful tax calculation via controller"""
        # Arrange
        mock_tax_calculation_service.calculate_tax = AsyncMock(return_value=sample_calculation_response)
        rule_type = "income_tax"
        amount = 50000.0
        
        # Act
        result = await tax_controller.calculate_tax(rule_type, amount)
        
        # Assert
        assert isinstance(result, TaxCalculationResponse)
        assert result.income == 50000.0
        assert result.tax_amount == 10000.0
        assert result.rule_version == "1.0"
        mock_tax_calculation_service.calculate_tax.assert_called_once_with(amount, rule_type)
    
    @pytest.mark.asyncio
    async def test_calculate_tax_business_exception(self, tax_controller, mock_tax_calculation_service):
        """Test API handling of business exceptions"""
        # Arrange
        mock_tax_calculation_service.calculate_tax = AsyncMock(
            side_effect=BusinessException("No tax rule found for sales_tax")
        )
        rule_type = "sales_tax"
        amount = 1000.0
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await tax_controller.calculate_tax(rule_type, amount)
        
        assert exc_info.value.status_code == 422
        assert "failed" in exc_info.value.detail["message"]
    
    @pytest.mark.asyncio
    async def test_calculate_tax_unexpected_error(self, tax_controller, mock_tax_calculation_service):
        """Test API handling of unexpected errors"""
        # Arrange
        mock_tax_calculation_service.calculate_tax = AsyncMock(
            side_effect=Exception("Database connection failed")
        )
        rule_type = "income_tax"
        amount = 50000.0
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await tax_controller.calculate_tax(rule_type, amount)
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.detail["error_code"] == "INTERNAL_ERROR"


