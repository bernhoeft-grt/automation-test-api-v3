"""Test DELETE /api/v1/contratada-contrato/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("ContratadaContrato")
@allure.story("DELETE /api/v1/contratada-contrato/{id}")
class TestDeleteContratadaContrato:
    """Test DELETE Contratada Contrato."""
    
    @allure.title("Delete Contratada Contrato")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Contratada Contrato."""
        from tests.contratada_contrato.resource import ContratadaContratoResource
        
        page = ContratadaContratoResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/contratada-contrato/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/contratada-contrato/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
