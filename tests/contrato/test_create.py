"""Test POST /api/v1/contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_object_payload_schema, assert_status_code


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
        data = {
            "numero": "TEST-001",
            "Descricao": "Test Description",
            "DataInicio": "2024-01-01T00:00:00Z"
        }

        with allure.step("Make POST request to /api/v1/contrato"):
            response = page.create(data)
            attach_request("POST", "/contrato", data)
            attach_response(response, "Create Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 201)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response)
