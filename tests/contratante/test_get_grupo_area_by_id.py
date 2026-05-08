"""Test GET /api/v1/contratante/{id}/grupo-area/{grupo-area-id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id, get_object_payload


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
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                grupo_area_id = 1
                with allure.step(f"Make GET request to /api/v1/contratante/{test_id}/grupo-area/{grupo_area_id}"):
                    response = page.get_grupo_area_by_id(test_id, grupo_area_id)
                    attach_request("GET", f"/contratante/{test_id}/grupo-area/{grupo_area_id}")
                    attach_response(response, "Get Grupo Area By ID Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 404]
                if response.status_code == 200:
                    with allure.step("Validate response schema (200)"):
                        payload = get_object_payload(response)
                        assert isinstance(payload, dict), (
                            f"GET by ID deveria retornar um objeto JSON (dict), retornou: {type(payload)}"
                        )
                        assert len(payload) > 0, "GET by ID deveria retornar um objeto não vazio"
                        payload_id = payload.get("Id") or payload.get("id") or payload.get("GrupoAreaId")
                        if payload_id is not None:
                            assert payload_id == grupo_area_id, (
                                f"GET by ID deveria retornar Id={grupo_area_id}, retornou {payload_id}"
                            )
