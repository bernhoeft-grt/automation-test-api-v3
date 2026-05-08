"""Test POST /api/v1/area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("Area")
@allure.story("POST /api/v1/area")
class TestCreateArea:
    """Test POST create Area."""
    
    @allure.title("Create Area")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Area."""
        from tests.area.resource import AreaResource
        
        page = AreaResource(api_client)
        data = {"nome": "Test Area", "descricao": "Test Description"}
        
        with allure.step("Make POST request to /api/v1/area"):
            response = page.create(data)
            attach_request("POST", "/area", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]