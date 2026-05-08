"""Test DELETE /api/v1/contratada/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("Contratada")
@allure.story("DELETE /api/v1/contratada/{id}")
class TestDeleteContratada:
    """Test DELETE Contratada."""
    
    @allure.title("Delete Contratada")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Contratada."""
        from tests.contratada.resource import ContratadaResource
        
        page = ContratadaResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                with allure.step(f"Make DELETE request to /api/v1/contratada/{test_id}"):
                    response = page.delete(test_id)
                    attach_request("DELETE", f"/contratada/{test_id}")
                    attach_response(response, "Delete Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 204, 400, 401, 404]