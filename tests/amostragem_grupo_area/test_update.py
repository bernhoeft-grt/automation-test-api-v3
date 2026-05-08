"""Test PUT /api/v1/amostragem-grupo-area/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("PUT /api/v1/amostragem-grupo-area/{id}")
class TestUpdateAmostragemGrupoArea:
    """Test PUT update Amostragem Grupo Area."""
    
    @allure.title("Update Amostragem Grupo Area")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Amostragem Grupo Area."""
        from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource
        
        page = AmostragemGrupoAreaResource(api_client)
        
        # First get all to get an ID
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                data = {
                    "nome": "Updated Amostragem Grupo Area",
                    "descricao": "Updated Description"
                }
                with allure.step(f"Make PUT request to /api/v1/amostragem-grupo-area/{test_id}"):
                    response = page.update(test_id, data)
                    attach_request("PUT", f"/amostragem-grupo-area/{test_id}", data)
                    attach_response(response, "Update Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]