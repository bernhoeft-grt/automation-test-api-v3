"""Test GET /api/v1/amostragem-grupo-area/{id}."""
import allure
import pytest
from utils.helpers import (
    attach_request,
    attach_response,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
)
from tests.amostragem_grupo_area.resource import AmostragemGrupoAreaResource


@allure.epic("ContractWeb API")
@allure.feature("AmostragemGrupoArea")
@allure.story("GET /api/v1/amostragem-grupo-area/{id}")
class TestGetAmostragemGrupoAreaById:
    """Test GET Amostragem Grupo Area by ID."""

    @allure.title("Get Amostragem Grupo Area by ID")
    @pytest.mark.api
    def test_get_by_id(self, api_client):
        """Test getting Amostragem Grupo Area by ID."""
        page = AmostragemGrupoAreaResource(api_client)

        test_id = get_existing_resource_id(page.get_all())
        with allure.step(f"Make GET request to /api/v1/amostragem-grupo-area/{test_id}"):
            response = page.get_by_id(test_id)
            attach_request("GET", f"/amostragem-grupo-area/{test_id}")
            attach_response(response, "Get By ID Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(
                response,
                required_keys=[
                    "Id",
                    "Ativo",
                    "Tipo",
                    "FaixaInicio",
                    "FaixaFinal",
                    "AmostragemSolicitacao",
                    "TipoAmostragemSolicitacao",
                    "AmostragemAdmissao",
                    "TipoAmostragemAdmissao",
                    "AmostragemDemissao",
                    "TipoAmostragemDemissao",
                    "AmostragemAtivos",
                    "TipoAmostragemAtivos",
                    "AmostragemMinimo",
                    "AmostragemMaxima",
                    "GrupoAreaId",
                ],
                expected_id=test_id,
            )
