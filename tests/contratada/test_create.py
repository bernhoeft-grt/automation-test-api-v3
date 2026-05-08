"""Test POST /api/v1/contratada."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("Contratada")
@allure.story("POST /api/v1/contratada")
class TestCreateContratada:
    """Test POST create Contratada."""
    
    @allure.title("Create Contratada")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Contratada."""
        from tests.contratada.resource import ContratadaResource
        
        page = ContratadaResource(api_client)
        data = {"nome": "Test Contratada", "descricao": "Test Description"}
        
        with allure.step("Make POST request to /api/v1/contratada"):
            response = page.create(data)
            attach_request("POST", "/contratada", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]