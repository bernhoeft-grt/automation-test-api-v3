"""Test GET /api/v1/contratante/{id}/familia."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_list_payload, assert_status_code, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("Contratante")
@allure.story("GET /api/v1/contratante/{id}/familia")
class TestGetContratanteFamilia:
    """Test GET Contratante Familia."""
    
    @allure.title("Get Familia IDs atrelados a Contratante")
    @pytest.mark.api
    def test_get_familia(self, api_client):
        """Test getting Familia IDs atrelados a Contratante."""
        from tests.contratante.resource import ContratanteResource
        
        page = ContratanteResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make GET request to /api/v1/contratante/{test_id}/familia"):
            response = page.get_familia(test_id)
            attach_request("GET", f"/contratante/{test_id}/familia")
            attach_response(response, "Get Familia Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            items = assert_list_payload(response)
            if len(items) > 0:
                first_item = items[0]
                assert isinstance(first_item, (int, dict)), (
                    "Primeiro item deveria ser int ou objeto (dict)"
                )
                if isinstance(first_item, dict):
                    assert "Id" in first_item or "id" in first_item, (
                        "Item deveria conter a chave 'Id' ou 'id'"
                    )
