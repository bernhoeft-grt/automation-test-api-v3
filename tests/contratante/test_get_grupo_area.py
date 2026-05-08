"""Test GET /api/v1/contratante/{id}/grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id, assert_list_payload


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("GET /api/v1/contratante/{id}/grupo-area")
class TestGetContratanteGrupoArea:
    """Test GET Contratante Grupo Area."""
    
    @allure.title("Get Grupo Area atrelados a Contratante")
    @pytest.mark.api
    def test_get_grupo_area(self, api_client):
        """Test getting Grupo Area atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                with allure.step(f"Make GET request to /api/v1/contratante/{test_id}/grupo-area"):
                    response = page.get_grupo_area(test_id)
                    attach_request("GET", f"/contratante/{test_id}/grupo-area")
                    attach_response(response, "Get Grupo Area Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 404]
                if response.status_code == 200:
                    with allure.step("Validate response schema (200)"):
                        items = assert_list_payload(response)
                        if len(items) > 0:
                            first_item = items[0]
                            assert isinstance(first_item, dict), "Primeiro item deveria ser um objeto (dict)"
                            assert "Id" in first_item or "id" in first_item, (
                                "Item deveria conter a chave 'Id' ou 'id'"
                            )
