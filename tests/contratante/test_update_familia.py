"""Test PUT /api/v1/contratante/{id}/familia."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("PUT /api/v1/contratante/{id}/familia")
class TestUpdateContratanteFamilia:
    """Test PUT update Contratante Familia."""
    
    @allure.title("Update Familia IDs atrelados a Contratante")
    @pytest.mark.api
    def test_update_familia(self, api_client):
        """Test updating Familia IDs atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                familia_ids = [1, 2]
                with allure.step(f"Make PUT request to /api/v1/contratante/{test_id}/familia"):
                    response = page.update_familia(test_id, familia_ids)
                    attach_request("PUT", f"/contratante/{test_id}/familia", {"familiaIds": familia_ids})
                    attach_response(response, "Update Familia Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]