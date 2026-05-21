"""Test GET /api/v1/classificacao-colaborador/{id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
)


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("GET /api/v1/classificacao-colaborador/{id}")
class TestGetClassificacaoColaboradorById:
    """Test GET Classificacao Colaborador by ID."""
    
    @allure.title("Get Classificacao Colaborador by ID")
    @pytest.mark.api
    def test_get_by_id(self, api_client):
        """Test getting Classificacao Colaborador by ID."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make GET request to /api/v1/classificacao-colaborador/{test_id}"):
            response = page.get_by_id(test_id)
            attach_request("GET", f"/classificacao-colaborador/{test_id}")
            attach_response(response, "Get By ID Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response, required_keys=["Id"], expected_id=test_id)
