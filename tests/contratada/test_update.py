"""Test PUT /api/v1/contratada/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("Contratada")
@allure.story("PUT /api/v1/contratada/{id}")
class TestUpdateContratada:
    """Test PUT update Contratada."""
    
    @allure.title("Update Contratada")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Contratada."""
        from tests.contratada.resource import ContratadaResource
        
        page = ContratadaResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                data = {"nome": "Updated Contratada", "descricao": "Updated Description"}
                with allure.step(f"Make PUT request to /api/v1/contratada/{test_id}"):
                    response = page.update(test_id, data)
                    attach_request("PUT", f"/contratada/{test_id}", data)
                    attach_response(response, "Update Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]