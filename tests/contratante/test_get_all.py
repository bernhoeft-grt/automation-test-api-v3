"""Test GET /api/v1/contratante."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("GET /api/v1/contratante")
class TestGetAllContratante:
    """Test GET all Contratantes."""
    
    @allure.title("Get all Contratantes")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Contratantes."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        with allure.step("Make GET request to /api/v1/contratante"):
            response = page.get_all()
            attach_request("GET", "/contratante")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
