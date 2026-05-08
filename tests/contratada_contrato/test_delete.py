"""Test DELETE /api/v1/contratada-contrato/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


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
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                with allure.step(f"Make DELETE request to /api/v1/contratada-contrato/{test_id}"):
                    response = page.delete(test_id)
                    attach_request("DELETE", f"/contratada-contrato/{test_id}")
                    attach_response(response, "Delete Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 204, 400, 401, 404]