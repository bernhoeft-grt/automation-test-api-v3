"""Test POST /api/v1/contratante."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_object_payload_schema, assert_status_code


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
        data = {
            "nome": "Test Contratante",
            "Descricao": "Test Description",
            "TipoPessoa": "PJ"
        }
        
        with allure.step("Make POST request to /api/v1/contratante"):
            response = page.create(data)
            attach_request("POST", "/contratante", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 201)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response)
