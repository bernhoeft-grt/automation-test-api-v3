"""Test PUT /api/v1/contratante/{id}/grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_json_response, assert_list_payload, assert_status_code, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("PUT /api/v1/contratante/{id}/grupo-area")
class TestUpdateContratanteGrupoArea:
    """Test PUT update Contratante Grupo Area."""
    
    @allure.title("Update Grupo Area IDs atrelados a Contratante")
    @pytest.mark.api
    def test_update_grupo_area(self, api_client):
        """Test updating Grupo Area IDs atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        grupo_area_response = page.get_grupo_area(test_id)
        assert_status_code(grupo_area_response, 200, context="Verify GET grupo-area response status code")
        grupo_area_items = assert_list_payload(grupo_area_response)
        if len(grupo_area_items) == 0:
            pytest.skip("Contratante sem grupo-area relacionado no ambiente")

        grupo_area_ids = [
            item.get("Id") or item.get("id")
            for item in grupo_area_items
            if isinstance(item, dict)
        ]
        grupo_area_ids = [item_id for item_id in grupo_area_ids if item_id is not None]
        if len(grupo_area_ids) == 0:
            pytest.skip("GET grupo-area não retornou identificadores válidos")

        with allure.step(f"Make PUT request to /api/v1/contratante/{test_id}/grupo-area"):
            response = page.update_grupo_area(test_id, grupo_area_ids)
            attach_request("PUT", f"/contratante/{test_id}/grupo-area", {"grupoAreaIds": grupo_area_ids})
            attach_response(response, "Update Grupo Area Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, [200, 204])

        with allure.step("Validate response schema when body exists"):
            if response.status_code == 200 and response.text.strip():
                assert_json_response(response)
