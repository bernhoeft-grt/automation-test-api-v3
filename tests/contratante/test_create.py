"""Test POST /api/v1/contratante."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("POST /api/v1/contratante")
class TestCreateContratante:
    """Test POST create Contratante."""
    
    @allure.title("Create Contratante")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        data = {"nome": "Test Contratante", "descricao": "Test Description"}
        
        with allure.step("Make POST request to /api/v1/contratante"):
            response = page.create(data)
            attach_request("POST", "/contratante", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]