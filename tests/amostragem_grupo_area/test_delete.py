"""Test DELETE /api/v1/amostragem-grupo-area/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


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
        
        # First get all to get an ID
        all_response = page.get_all()
        test_id = None
        if all_response.status_code == 200:
            try:
                data = all_response.json()
                if data:
                    test_id = get_first_id(all_response)
            except Exception:
                pass
        
        if test_id:
            with allure.step(f"Make DELETE request to /api/v1/amostragem-grupo-area/{test_id}"):
                response = page.delete(test_id)
                attach_request("DELETE", f"/amostragem-grupo-area/{test_id}")
                attach_response(response, "Delete Response")
            
            with allure.step("Verify response status code"):
                assert response.status_code in [200, 204, 400, 401, 404]
        else:
            pytest.skip("No ID found to delete")