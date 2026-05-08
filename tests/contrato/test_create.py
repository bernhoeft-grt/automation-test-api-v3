"""Test POST /api/v1/contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("POST /api/v1/contrato")
class TestCreateContrato:
    """Test POST create Contrato."""

    @allure.title("Create Contrato")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Contrato."""
        from tests.contrato.resource import ContratoResource

        page = ContratoResource(api_client)
        data = {"numero": "TEST-001", "descricao": "Test Description"}

        with allure.step("Make POST request to /api/v1/contrato"):
            response = page.create(data)
            attach_request("POST", "/contrato", data)
            attach_response(response, "Create Response")

        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]
