"""Test POST /api/v1/avisos."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_object_payload_schema, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("Avisos")
@allure.story("POST /api/v1/avisos")
class TestCreateAvisos:
    """Test POST create Aviso."""
    
    @allure.title("Create Aviso")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Aviso."""
        from tests.avisos.resource import AvisosResource
        
        page = AvisosResource(api_client)
        data = {"titulo": "Test Aviso", "descricao": "Test Description"}
        
        with allure.step("Make POST request to /api/v1/avisos"):
            response = page.create(data)
            attach_request("POST", "/avisos", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 201)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response)
