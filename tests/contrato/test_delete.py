"""Test DELETE /api/v1/contrato/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("DELETE /api/v1/contrato/{id}")
class TestDeleteContrato:
    """Test DELETE Contrato."""
    
    @allure.title("Delete Contrato")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Contrato."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/contrato/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/contrato/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
