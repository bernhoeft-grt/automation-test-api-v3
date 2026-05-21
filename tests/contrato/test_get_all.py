"""Test GET /api/v1/contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("GET /api/v1/contrato")
class TestGetAllContrato:
    """Test GET all Contratos."""
    
    @allure.title("Get all Contratos")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Contratos."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        with allure.step("Make GET request to /api/v1/contrato"):
            response = page.get_all()
            attach_request("GET", "/contrato")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
