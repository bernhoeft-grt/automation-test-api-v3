"""Test DELETE /api/v1/amostragem-grupo-area/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("DELETE /api/v1/amostragem-grupo-area/{id}")
class TestDeleteAmostragemGrupoArea:
    """Test DELETE Amostragem Grupo Area."""
    
    @allure.title("Delete Amostragem Grupo Area")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Amostragem Grupo Area."""
        from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource
        
        page = AmostragemGrupoAreaResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/amostragem-grupo-area/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/amostragem-grupo-area/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
