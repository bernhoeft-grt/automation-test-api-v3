"""Test PUT /api/v1/contratante/{id}/familia."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_json_response, assert_list_payload, assert_status_code, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("PUT /api/v1/contratante/{id}/familia")
class TestUpdateContratanteFamilia:
    """Test PUT update Contratante Familia."""
    
    @allure.title("Update Familia IDs atrelados a Contratante")
    @pytest.mark.api
    def test_update_familia(self, api_client):
        """Test updating Familia IDs atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        familia_response = page.get_familia(test_id)
        assert_status_code(familia_response, 200, context="Verify GET familia response status code")
        familia_items = assert_list_payload(familia_response)
        if len(familia_items) == 0:
            pytest.skip("Contratante sem familia relacionada no ambiente")

        familia_ids = [
            item if isinstance(item, int) else item.get("Id") or item.get("id")
            for item in familia_items
        ]
        familia_ids = [item_id for item_id in familia_ids if item_id is not None]
        if len(familia_ids) == 0:
            pytest.skip("GET familia não retornou identificadores válidos")

        with allure.step(f"Make PUT request to /api/v1/contratante/{test_id}/familia"):
            response = page.update_familia(test_id, familia_ids)
            attach_request("PUT", f"/contratante/{test_id}/familia", {"familiaIds": familia_ids})
            attach_response(response, "Update Familia Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, [200, 204])

        with allure.step("Validate response schema when body exists"):
            if response.status_code == 200 and response.text.strip():
                assert_json_response(response)
