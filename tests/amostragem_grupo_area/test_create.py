"""Test POST /api/v1/amostragem-grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_object_payload_schema, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("POST /api/v1/amostragem-grupo-area")
class TestCreateAmostragemGrupoArea:
    """Test POST create Amostragem Grupo Area."""
    
    @allure.title("Create Amostragem Grupo Area")
    @pytest.mark.api
    def test_create(self, api_client):
        """Test creating Amostragem Grupo Area."""
        from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource
        
        page = AmostragemGrupoAreaResource(api_client)
        data = {
            "nome": "Test Amostragem Grupo Area",
            "descricao": "Test Description"
        }
        
        with allure.step("Make POST request to /api/v1/amostragem-grupo-area"):
            response = page.create(data)
            attach_request("POST", "/amostragem-grupo-area", data)
            attach_response(response, "Create Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 201)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response)
