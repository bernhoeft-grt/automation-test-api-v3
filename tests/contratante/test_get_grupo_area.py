"""Test GET /api/v1/contratante/{id}/grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_payload, assert_status_code, get_existing_resource_id


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
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make GET request to /api/v1/contratante/{test_id}/grupo-area"):
            response = page.get_grupo_area(test_id)
            attach_request("GET", f"/contratante/{test_id}/grupo-area")
            attach_response(response, "Get Grupo Area Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            items = assert_list_payload(response)
            if len(items) > 0:
                first_item = items[0]
                assert isinstance(first_item, dict), "Primeiro item deveria ser um objeto (dict)"
                assert "Id" in first_item or "id" in first_item, (
                    "Item deveria conter a chave 'Id' ou 'id'"
                )
