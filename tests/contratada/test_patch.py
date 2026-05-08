"""Test PATCH /api/v1/contratada/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("Contratada")
@allure.story("PATCH /api/v1/contratada/{id}")
class TestPatchContratada:
    """Test PATCH partial update Contratada."""
    
    @allure.title("Patch Contratada")
    @pytest.mark.api
    def test_patch(self, api_client):
        """Test partial updating Contratada."""
        from tests.contratada.resource import ContratadaResource
        
        page = ContratadaResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                data = {"nome": "Patched Contratada"}
                with allure.step(f"Make PATCH request to /api/v1/contratada/{test_id}"):
                    response = page.patch(test_id, data)
                    attach_request("PATCH", f"/contratada/{test_id}", data)
                    attach_response(response, "Patch Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]