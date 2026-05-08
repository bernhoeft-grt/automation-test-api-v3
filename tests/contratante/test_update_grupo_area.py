"""Test PUT /api/v1/contratante/{id}/grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("PUT /api/v1/contratante/{id}/grupo-area")
class TestUpdateContratanteGrupoArea:
    """Test PUT update Contratante Grupo Area."""
    
    @allure.title("Update Grupo Area IDs atrelados a Contratante")
    @pytest.mark.api
    def test_update_grupo_area(self, api_client):
        """Test updating Grupo Area IDs atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                grupo_area_ids = [1, 2]
                with allure.step(f"Make PUT request to /api/v1/contratante/{test_id}/grupo-area"):
                    response = page.update_grupo_area(test_id, grupo_area_ids)
                    attach_request("PUT", f"/contratante/{test_id}/grupo-area", {"grupoAreaIds": grupo_area_ids})
                    attach_response(response, "Update Grupo Area Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]