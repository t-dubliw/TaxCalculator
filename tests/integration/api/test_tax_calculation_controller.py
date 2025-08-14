


"""
Test cases for Tax Calculation Controller API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock
from fastapi import FastAPI, status

from src.infrastructure.configuration.dependency_injection import get_tax_calculation_controller
from src.presentation.api.v1.controllers.tax_calculation_controller import (
    router,
    TaxCalculationController
)
from src.presentation.api.v1.schemas.response.tax_calculation_response import (
    TaxCalculationResponse
)
from src.shared.exceptions.base_exceptions import (
    BusinessException,
    ValidationException
)

class TestTaxCalculationController:
    """Test suite for tax calculation API endpoints"""

    @pytest.fixture
    def mock_service(self):
        """Mock TaxCalculationService"""
        service = Mock()
        service.calculate_tax = AsyncMock()
        return service

    @pytest.fixture
    def client(self, mock_service):
        """Test client with mocked dependencies"""
        app = FastAPI()
        app.include_router(router)
        
        def get_controller():
            return TaxCalculationController(mock_service)
        
        app.dependency_overrides[get_tax_calculation_controller] = get_controller
        return TestClient(app)

    @pytest.fixture
    def sample_success_response(self):
        """Sample successful tax calculation response"""
        return TaxCalculationResponse(
            income=122.0,
            tax_amount=12.2,
            rule_version="2024.1",
            breakdown=[{
                "bracket": "0-520.5",
                "rate": "10.00%",
                "taxable_amount": "122.00",
                "tax": "12.20"
            }]
        )

    def test_calculate_tax_success(
        self, 
        client, 
        mock_service, 
        sample_success_response
    ):
        """
        Test successful tax calculation returns correct response
        """
        # Arrange
        mock_service.calculate_tax.return_value = sample_success_response
        url = "/tax-rules/calculate/income_tax/1000.0"

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["income"] == 1000.0
        assert data["tax_amount"] == 200.0
        assert data["rule_version"] == "1.0"
        # assert data["success"] is True
        mock_service.calculate_tax.assert_called_once_with(1000.0, "income_tax")

    def test_calculate_tax_validation_error(self, client, mock_service):
        """
        Test invalid input returns validation error
        """
        # Arrange
        mock_service.calculate_tax.side_effect = ValidationException(
            "Amount must be positive"
        )
        url = "/tax-rules/calculate/income_tax/-100.0"

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert data["detail"]["error_code"] == "VALIDATION_ERROR"
        assert "must be positive" in data["detail"]["details"]

    def test_calculate_tax_business_error(self, client, mock_service):
        """
        Test invalid rule type returns business error
        """
        # Arrange
        mock_service.calculate_tax.side_effect = BusinessException(
            "No tax rule found for type: invalid_type"
        )
        url = "/tax-rules/calculate/invalid_type/1000.0"

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert data["detail"]["error_code"] == "BUSINESS_ERROR"
        assert "No tax rule found" in data["detail"]["message"]

    def test_calculate_tax_internal_error(self, client, mock_service):
        """
        Test unexpected errors return 500 status
        """
        # Arrange
        mock_service.calculate_tax.side_effect = Exception("Database error")
        url = "/tax-rules/calculate/income_tax/1000.0"

        # Act
        response = client.get(url)

        # Assert
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        data = response.json()
        assert data["detail"]["error_code"] == "INTERNAL_ERROR"

    def test_calculate_tax_with_different_rule_types(
        self, 
        client, 
        mock_service,
        sample_success_response
    ):
        """
        Test different tax rule types are handled correctly
        """
        # Arrange
        mock_service.calculate_tax.return_value = sample_success_response
        test_cases = [
            ("sales_tax", 500.0),
            ("vat", 750.0),
            ("property_tax", 1200.0)
        ]

        for rule_type, amount in test_cases:
            url = f"/tax-rules/calculate/{rule_type}/{amount}"

            # Act
            response = client.get(url)

            # Assert
            assert response.status_code == status.HTTP_200_OK
            mock_service.calculate_tax.assert_called_with(amount, rule_type)
            mock_service.calculate_tax.reset_mock()

    def test_calculate_tax_with_edge_case_amounts(
        self,
        client,
        mock_service,
        sample_success_response
    ):
        """
        Test edge case amount values
        """
        # Arrange
        mock_service.calculate_tax.return_value = sample_success_response
        test_cases = [
            (0.0, "Zero amount"),
            (1e6, "Large amount"),
            (0.01, "Small amount")
        ]

        for amount, desc in test_cases:
            url = f"/tax-rules/calculate/income_tax/{amount}"

            # Act
            response = client.get(url)

            # Assert
            assert response.status_code == status.HTTP_200_OK, f"Failed for {desc}"
            mock_service.calculate_tax.assert_called_with(amount, "income_tax")
            mock_service.calculate_tax.reset_mock()