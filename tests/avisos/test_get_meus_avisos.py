"""Test GET /api/v1/avisos/meus-avisos."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_payload


@allure.epic("ContractWeb API")
@allure.feature("Avisos")
@allure.story("GET /api/v1/avisos/meus-avisos")
class TestGetMeusAvisos:
    """Test GET meus avisos."""
    
    @allure.title("Get Avisos do Operador Autenticado")
    @pytest.mark.api
    def test_get_meus_avisos(self, api_client):
        """Test getting Avisos do Operador Autenticado."""
        from tests.avisos.resource import AvisosResource
        
        page = AvisosResource(api_client)
        
        with allure.step("Make GET request to /api/v1/avisos/meus-avisos"):
            response = page.get_meus_avisos()
            attach_request("GET", "/avisos/meus-avisos")
            attach_response(response, "Get Meus Avisos Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 401]
        if response.status_code == 200:
            with allure.step("Validate response schema (200)"):
                items = assert_list_payload(response)
                if len(items) > 0:
                    first_item = items[0]
                    assert isinstance(first_item, dict), "Primeiro item deveria ser um objeto (dict)"
                    assert "Id" in first_item or "id" in first_item, (
                        "Item deveria conter a chave 'Id' ou 'id'"
                    )
