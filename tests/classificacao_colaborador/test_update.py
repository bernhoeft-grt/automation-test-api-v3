"""Test PUT /api/v1/classificacao-colaborador/{id}."""
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
@allure.story("PUT /api/v1/classificacao-colaborador/{id}")
class TestUpdateClassificacaoColaborador:
    """Test PUT update Classificacao Colaborador."""
    
    @allure.title("Update Classificacao Colaborador")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Classificacao Colaborador."""
        from tests.classificacao_colaborador.resource import ClassificacaoColaboradorResource
        
        page = ClassificacaoColaboradorResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        data = {"nome": "Updated Classificacao", "Descricao": "Updated Description"}
        with allure.step(f"Make PUT request to /api/v1/classificacao-colaborador/{test_id}"):
            response = page.update(test_id, data)
            attach_request("PUT", f"/classificacao-colaborador/{test_id}", data)
            attach_response(response, "Update Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response, required_keys=["Id"], expected_id=test_id)
