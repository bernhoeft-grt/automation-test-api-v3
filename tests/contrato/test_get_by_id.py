"""Test GET /api/v1/contrato/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id, get_object_payload


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("GET /api/v1/contrato/{id}")
class TestGetContratoById:
    """Test GET Contrato by ID."""
    
    @allure.title("Get Contrato by ID")
    @pytest.mark.api
    def test_get_by_id(self, api_client):
        """Test getting Contrato by ID."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                with allure.step(f"Make GET request to /api/v1/contrato/{test_id}"):
                    response = page.get_by_id(test_id)
                    attach_request("GET", f"/contrato/{test_id}")
                    attach_response(response, "Get By ID Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 404]
                if response.status_code == 200:
                    with allure.step("Validate response schema (200)"):
                        payload = get_object_payload(response)
                        assert isinstance(payload, dict), (
                            f"GET by ID deveria retornar um objeto JSON (dict), retornou: {type(payload)}"
                        )
                        assert "Id" in payload or "id" in payload, (
                            "GET by ID deveria conter a chave 'Id' ou 'id'"
                        )
                        payload_id = payload.get("Id") or payload.get("id")
                        assert payload_id == test_id, (
                            f"GET by ID deveria retornar Id={test_id}, retornou {payload_id}"
                        )
