"""Test DELETE /api/v1/contratada/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


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
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/contratada/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/contratada/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
