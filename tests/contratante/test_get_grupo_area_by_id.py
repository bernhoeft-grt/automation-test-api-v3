"""Test GET /api/v1/contratante/{id}/grupo-area/{grupo-area-id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_list_payload,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
)


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("GET /api/v1/contratante/{id}/grupo-area/{grupo-area-id}")
class TestGetContratanteGrupoAreaById:
    """Test GET Contratante Grupo Area by ID."""
    
    @allure.title("Get Objetos de Mobilização do Grupo de Area atrelados a Contratante")
    @pytest.mark.api
    def test_get_grupo_area_by_id(self, api_client):
        """Test getting Objetos de Mobilização do Grupo de Area atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        grupo_area_response = page.get_grupo_area(test_id)
        assert_status_code(grupo_area_response, 200, context="Verify GET grupo-area response status code")
        grupo_area_items = assert_list_payload(grupo_area_response)
        if len(grupo_area_items) == 0:
            pytest.skip("Contratante sem grupo-area relacionado no ambiente")

        first_item = grupo_area_items[0]
        if not isinstance(first_item, dict):
            pytest.skip("GET grupo-area não retornou objetos com identificador para o cenário by-id")

        grupo_area_id = first_item.get("Id") or first_item.get("id")
        if grupo_area_id is None:
            pytest.skip("GET grupo-area não retornou chave Id/id para o cenário by-id")

        with allure.step(f"Make GET request to /api/v1/contratante/{test_id}/grupo-area/{grupo_area_id}"):
            response = page.get_grupo_area_by_id(test_id, grupo_area_id)
            attach_request("GET", f"/contratante/{test_id}/grupo-area/{grupo_area_id}")
            attach_response(response, "Get Grupo Area By ID Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response)
