"""Test PUT /api/v1/contratada-contrato/{id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
    get_list_payload,
)


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
        test_id = get_existing_resource_id(all_response)
        first_item = get_list_payload(all_response)[0]
        data = {
            "contratadaId": first_item.get("ContratadaId", 1),
            "contratoId": first_item.get("ContratoId", 1),
        }
        with allure.step(f"Make PUT request to /api/v1/contratada-contrato/{test_id}"):
            response = page.update(test_id, data)
            attach_request("PUT", f"/contratada-contrato/{test_id}", data)
            attach_response(response, "Update Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response, required_keys=["Id"], expected_id=test_id)
