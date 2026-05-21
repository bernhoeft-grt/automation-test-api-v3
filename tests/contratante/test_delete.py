"""Test DELETE /api/v1/contratante/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("DELETE /api/v1/contratante/{id}")
class TestDeleteContratante:
    """Test DELETE Contratante."""
    
    @allure.title("Delete Contratante")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/contratante/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/contratante/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
