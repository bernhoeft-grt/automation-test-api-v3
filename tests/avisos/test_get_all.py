"""Test GET /api/v1/avisos."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("Avisos")
@allure.story("GET /api/v1/avisos")
class TestGetAllAvisos:
    """Test GET all Avisos."""
    
    @allure.title("Get all Avisos")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Avisos."""
        from tests.avisos.resource import AvisosResource
        
        page = AvisosResource(api_client)
        
        with allure.step("Make GET request to /api/v1/avisos"):
            response = page.get_all()
            attach_request("GET", "/avisos")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
