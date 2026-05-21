"""Test GET /api/v1/contrato/{id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
)


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("GET /api/v1/contrato/{id}")
class TestGetContratoById:
    """Test GET Contrato by ID."""
    
    @allure.title("Get Contrato by ID")
    @pytest.mark.api
    def test_get_by_id(self, api_client):
        """Test getting Contrato by ID."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make GET request to /api/v1/contrato/{test_id}"):
            response = page.get_by_id(test_id)
            attach_request("GET", f"/contrato/{test_id}")
            attach_response(response, "Get By ID Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response, required_keys=["Id"], expected_id=test_id)
