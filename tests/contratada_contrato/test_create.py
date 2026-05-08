"""Test POST /api/v1/contratada-contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("ContratadaContrato")
@allure.story("POST /api/v1/contratada-contrato")
class TestCreateContratadaContrato:
    """Test POST create Contratada Contrato."""
    
    @allure.title("Create Contratada Contrato")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Contratada Contrato."""
        from tests.contratada_contrato.resource import ContratadaContratoResource
        
        page = ContratadaContratoResource(api_client)
        data = {"contratadaId": 1, "contratoId": 1}
        
        with allure.step("Make POST request to /api/v1/contratada-contrato"):
            response = page.create(data)
            attach_request("POST", "/contratada-contrato", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]