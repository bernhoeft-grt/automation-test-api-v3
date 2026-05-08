"""Test GET /api/v1/contratada/{id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_is_instance,
    assert_status_code,
    assert_true,
    get_first_id,
    get_object_payload,
)


@allure.epic("ContractWeb API")
@allure.feature("Contratada")
@allure.story("GET /api/v1/contratada/{id}")
class TestGetContratadaById:
    """Test GET Contratada by ID."""
    
    @allure.title("Get Contratada by ID")
    @pytest.mark.api
    def test_get_by_id(self, api_client):
        """Test getting Contratada by ID."""
        from tests.contratada.resource import ContratadaResource
        
        page = ContratadaResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                with allure.step(f"Make GET request to /api/v1/contratada/{test_id}"):
                    response = page.get_by_id(test_id)
                    attach_request("GET", f"/contratada/{test_id}")
                    attach_response(response, "Get By ID Response")
                
                with allure.step("Verify response status code"):
                    assert_status_code(response, [200, 404], context="Verify response status code")
                if response.status_code == 200:
                    with allure.step("Validate response schema (200)"):
                        payload = get_object_payload(response)
                        assert_is_instance(
                            payload,
                            dict,
                            f"GET by ID deveria retornar um objeto JSON (dict), retornou: {type(payload)}",
                        )
                        assert_true(
                            "Id" in payload or "id" in payload,
                            "GET by ID deveria conter a chave 'Id' ou 'id'",
                            actual=list(payload.keys()),
                        )
                        payload_id = payload.get("Id") or payload.get("id")
                        assert_true(
                            payload_id == test_id,
                            f"GET by ID deveria retornar Id={test_id}, retornou {payload_id}",
                            actual=payload_id,
                            expected=test_id,
                        )
