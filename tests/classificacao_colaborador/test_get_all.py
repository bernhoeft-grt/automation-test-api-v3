"""Test GET /api/v1/classificacao-colaborador."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_paginated_list_response, assert_status_code


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("GET /api/v1/classificacao-colaborador")
class TestGetAllClassificacaoColaborador:
    """Test GET all Classificacao Colaborador."""
    
    @allure.title("Get all Classificacao Colaborador")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_get_all(self, api_client):
        """Test getting all Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        with allure.step("Make GET request to /api/v1/classificacao-colaborador"):
            response = page.get_all()
            attach_request("GET", "/classificacao-colaborador")
            attach_response(response, "Get All Response")
        
        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_paginated_list_response(response, item_keys=["Id"])
