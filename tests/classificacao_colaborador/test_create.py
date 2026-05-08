"""Test POST /api/v1/classificacao-colaborador."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("POST /api/v1/classificacao-colaborador")
class TestCreateClassificacaoColaborador:
    """Test POST create Classificacao Colaborador."""
    
    @allure.title("Create Classificacao Colaborador")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        data = {"nome": "Test Classificacao", "descricao": "Test Description"}
        
        with allure.step("Make POST request to /api/v1/classificacao-colaborador"):
            response = page.create(data)
            attach_request("POST", "/classificacao-colaborador", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]