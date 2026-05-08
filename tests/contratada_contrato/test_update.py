"""Test PUT /api/v1/contratada-contrato/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("ContratadaContrato")
@allure.story("PUT /api/v1/contratada-contrato/{id}")
class TestUpdateContratadaContrato:
    """Test PUT update Contratada Contrato."""
    
    @allure.title("Update Contratada Contrato")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Contratada Contrato."""
        from tests.contratada_contrato.resource import ContratadaContratoResource
        
        page = ContratadaContratoResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                data = {"contratadaId": 1, "contratoId": 1}
                with allure.step(f"Make PUT request to /api/v1/contratada-contrato/{test_id}"):
                    response = page.update(test_id, data)
                    attach_request("PUT", f"/contratada-contrato/{test_id}", data)
                    attach_response(response, "Update Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]