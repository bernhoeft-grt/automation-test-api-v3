"""Test GET /api/v1/contratada-contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("ContratadaContrato")
@allure.story("GET /api/v1/contratada-contrato")
class TestGetAllContratadaContrato:
    """Test GET all Contratada Contrato."""
    
    @allure.title("Get all Contratada Contrato")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Contratada Contrato."""
        from tests.contratada_contrato.resource import ContratadaContratoResource
        
        page = ContratadaContratoResource(api_client)
        
        with allure.step("Make GET request to /api/v1/contratada-contrato"):
            response = page.get_all()
            attach_request("GET", "/contratada-contrato")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
