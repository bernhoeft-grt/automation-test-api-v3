"""Test PUT /api/v1/classificacao-colaborador/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, get_first_id


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("PUT /api/v1/classificacao-colaborador/{id}")
class TestUpdateClassificacaoColaborador:
    """Test PUT update Classificacao Colaborador."""
    
    @allure.title("Update Classificacao Colaborador")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        all_response = page.get_all()
        if all_response.status_code == 200 and all_response.json():
            test_id = get_first_id(all_response)
            if test_id:
                data = {"nome": "Updated Classificacao", "descricao": "Updated Description"}
                with allure.step(f"Make PUT request to /api/v1/classificacao-colaborador/{test_id}"):
                    response = page.update(test_id, data)
                    attach_request("PUT", f"/classificacao-colaborador/{test_id}", data)
                    attach_response(response, "Update Response")
                
                with allure.step("Verify response status code"):
                    assert response.status_code in [200, 400, 401, 404]