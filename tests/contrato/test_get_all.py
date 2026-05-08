"""Test GET /api/v1/contrato."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_schema, get_list_payload


@allure.epic("ContractWeb API")
@allure.feature("Contrato")
@allure.story("GET /api/v1/contrato")
class TestGetAllContrato:
    """Test GET all Contratos."""
    
    @allure.title("Get all Contratos")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Contratos."""
        from tests.contrato.resource import ContratoResource
        
        page = ContratoResource(api_client)
        
        with allure.step("Make GET request to /api/v1/contrato"):
            response = page.get_all()
            attach_request("GET", "/contrato")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code == 200

        with allure.step("Validate response schema"):
            assert_list_schema(response)
            items = get_list_payload(response)
            first_item = items[0]
            assert "Id" in first_item or "id" in first_item, (
                "Item de 'Dados' deveria conter a chave 'Id' ou 'id'"
            )
