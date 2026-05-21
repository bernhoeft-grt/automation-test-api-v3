"""Test GET /api/v1/area."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_paginated_list_response,
    assert_status_code,
)


@allure.epic("ContractWeb API")
@allure.feature("Area")
@allure.story("GET /api/v1/area")
class TestGetAllArea:
    """Test GET all Areas."""
    
    @allure.title("Get all Areas")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Areas."""
        from tests.area.resource import AreaResource
        
        page = AreaResource(api_client)
        
        with allure.step("Make GET request to /api/v1/area"):
            response = page.get_all()
            attach_request("GET", "/area")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200, context="Verify response status code")

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
