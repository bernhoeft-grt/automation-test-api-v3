"""Test GET /api/v1/classificacao-colaborador."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_schema, get_list_payload


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("GET /api/v1/classificacao-colaborador")
class TestGetAllClassificacaoColaborador:
    """Test GET all Classificacao Colaborador."""
    
    @allure.title("Get all Classificacao Colaborador")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        with allure.step("Make GET request to /api/v1/classificacao-colaborador"):
            response = page.get_all()
            attach_request("GET", "/classificacao-colaborador")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code == 200

        with allure.step("Validate response schema"):
            assert_list_schema(response)
            items = get_list_payload(response)
            first_item = items[0]
            assert "Id" in first_item or "id" in first_item, (
                "Item de 'Dados' deveria conter a chave 'Id' ou 'id'"
            )
