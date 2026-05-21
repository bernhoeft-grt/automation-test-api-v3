"""Test GET /api/v1/amostragem-grupo-area."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("GET /api/v1/amostragem-grupo-area")
class TestGetAllAmostragemGrupoArea:
    """Test GET all Amostragem Grupo Area."""
    
    @allure.title("Get all Amostragem Grupo Area")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Amostragem Grupo Area."""
        from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource
        
        page = AmostragemGrupoAreaResource(api_client)
        
        with allure.step("Make GET request to /api/v1/amostragem-grupo-area"):
            response = page.get_all()
            attach_request("GET", "/amostragem-grupo-area")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(
                response,
                item_keys=["Id", "Ativo", "Tipo", "DescricaoGrupoArea"],
            )
