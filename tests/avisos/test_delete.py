"""Test DELETE /api/v1/avisos/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Avisos")
@allure.story("DELETE /api/v1/avisos/{id}")
class TestDeleteAvisos:
    """Test DELETE Aviso."""
    
    @allure.title("Delete Aviso")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Aviso."""
        from tests.avisos.resource import AvisosResource
        
        page = AvisosResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/avisos/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/avisos/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
