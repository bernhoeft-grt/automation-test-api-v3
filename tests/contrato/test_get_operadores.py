"""Test GET /api/v1/contrato/{id}/contratada/{contratada_id}/operadores."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_payload, assert_status_code, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("GET /api/v1/contrato/{id}/contratada/{contratada_id}/operadores")
class TestGetContratoOperadores:
    """Test GET Contrato Operadores."""
    
    @allure.title("Get Operadores da Contratada do Contrato")
    @pytest.mark.api
    def test_get_operadores(self, api_client):
        """Test getting Operadores da Contratada do Contrato."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        contratada_id = 1
        with allure.step(f"Make GET request to /api/v1/contrato/{test_id}/contratada/{contratada_id}/operadores"):
            response = page.get_operadores(test_id, contratada_id)
            attach_request("GET", f"/contrato/{test_id}/contratada/{contratada_id}/operadores")
            attach_response(response, "Get Operadores Response")

        if response.status_code == 404:
            pytest.skip("Ambiente não possui relacionamento contrato/contratada para o cenário de operadores")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            items = assert_list_payload(response)
            if len(items) > 0:
                first_item = items[0]
                assert isinstance(first_item, dict), "Primeiro item deveria ser um objeto (dict)"
