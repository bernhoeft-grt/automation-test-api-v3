"""Test GET /api/v1/contrato/{id}/contratada/{contratada_id}/operadores."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id, assert_list_payload


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
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                contratada_id = 1
                with allure.step(f"Make GET request to /api/v1/contrato/{test_id}/contratada/{contratada_id}/operadores"):
                    response = page.get_operadores(test_id, contratada_id)
                    attach_request("GET", f"/contrato/{test_id}/contratada/{contratada_id}/operadores")
                    attach_response(response, "Get Operadores Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 404]
                if response.status_code == 200:
                    with allure.step("Validate response schema (200)"):
                        items = assert_list_payload(response)
                        if len(items) > 0:
                            first_item = items[0]
                            assert isinstance(first_item, dict), "Primeiro item deveria ser um objeto (dict)"
