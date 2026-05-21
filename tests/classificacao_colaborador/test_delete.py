"""Test DELETE /api/v1/classificacao-colaborador/{id}."""
import pytest
import allure
from utils.helpers import attach_response, attach_request, assert_delete_response, get_existing_resource_id


@allure.epic("ContractWeb API")
@allure.feature("ClassificacaoColaborador")
@allure.story("DELETE /api/v1/classificacao-colaborador/{id}")
class TestDeleteClassificacaoColaborador:
    """Test DELETE Classificacao Colaborador."""
    
    @allure.title("Delete Classificacao Colaborador")
    @pytest.mark.api
    def test_delete(self, api_client):
        """Test deleting Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make DELETE request to /api/v1/classificacao-colaborador/{test_id}"):
            response = page.delete(test_id)
            attach_request("DELETE", f"/classificacao-colaborador/{test_id}")
            attach_response(response, "Delete Response")

        assert_delete_response(response)
