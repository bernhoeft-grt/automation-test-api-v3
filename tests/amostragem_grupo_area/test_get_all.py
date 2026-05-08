"""Test GET /api/v1/amostragem-grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("GET /api/v1/amostragem-grupo-area")
class TestGetAllAmostragemGrupoArea:
    """Test GET all Amostragem Grupo Area."""
    
    @allure.title("Get all Amostragem Grupo Area")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Amostragem Grupo Area."""
        from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource
        
        page = AmostragemGrupoAreaResource(api_client)
        
        with allure.step("Make GET request to /api/v1/amostragem-grupo-area"):
            response = page.get_all()
            attach_request("GET", "/amostragem-grupo-area")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code == 200

        with allure.step("Validate response schema"):
            try:
                body = response.json()
            except Exception:
                pytest.fail("GET_ALL retornou body que não é JSON")

            assert isinstance(body, dict), (
                f"GET_ALL deveria retornar um objeto JSON (dict), retornou: {type(body)}"
            )
            for key in ["Dados", "QuantidadeTotal", "Paginas", "Quantidade", "Pagina"]:
                assert key in body, f"GET_ALL deveria conter a chave '{key}'"

            dados = body.get("Dados")
            assert isinstance(dados, list), "GET_ALL -> 'Dados' deveria ser uma lista"
            if len(dados) == 0:
                pytest.skip("GET_ALL retornou lista vazia em 'Dados' (sem dados no ambiente)")

            first_item = dados[0]
            assert isinstance(first_item, dict), "Primeiro item de 'Dados' deveria ser um objeto (dict)"
            for key in ["Id", "Ativo", "Tipo", "DescricaoGrupoArea"]:
                assert key in first_item, f"Item de 'Dados' deveria conter a chave '{key}'"
