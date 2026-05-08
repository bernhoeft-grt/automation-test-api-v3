"""Test GET /api/v1/amostragem-grupo-area/{id}."""
import allure
import pytest
from utils.helpers import attach_request, attach_response
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

        # -------------------------
        # GET ALL (para pegar um ID)
        # -------------------------
        with allure.step("GET /api/v1/amostragem-grupo-area (get_all)"):
            all_response = page.get_all()

            print("\n===== GET_ALL RESPONSE =====")
            print("STATUS:", all_response.status_code)
            print("BODY:", all_response.text)

            attach_request("GET", "/amostragem-grupo-area")
            attach_response(all_response, "Get All Response")

            # Assert status
            assert all_response.status_code == 200, (
                f"GET_ALL deveria retornar 200, retornou {all_response.status_code}"
            )

            # Assert JSON válido
            try:
                body = all_response.json()
            except Exception:
                pytest.fail("GET_ALL retornou body que não é JSON")

            # Asserts de contrato (estrutura esperada)
            assert isinstance(body, dict), (
                f"GET_ALL deveria retornar um objeto JSON (dict), retornou: {type(body)}"
            )
            assert "Dados" in body, "GET_ALL deveria conter a chave 'Dados'"
            assert "QuantidadeTotal" in body, "GET_ALL deveria conter a chave 'QuantidadeTotal'"
            assert "Paginas" in body, "GET_ALL deveria conter a chave 'Paginas'"
            assert "Quantidade" in body, "GET_ALL deveria conter a chave 'Quantidade'"
            assert "Pagina" in body, "GET_ALL deveria conter a chave 'Pagina'"

            data = body.get("Dados")

            # Assert lista e não vazia
            if not isinstance(data, list) or len(data) == 0:
                pytest.skip("GET_ALL retornou lista vazia em 'Dados' (sem dados no ambiente)")

            # Assert item mínimo
            first_item = data[0]
            assert isinstance(first_item, dict), "Primeiro item de 'Dados' deveria ser um objeto (dict)"
            assert "Id" in first_item, "Primeiro item de 'Dados' deveria conter a chave 'Id'"

            test_id = first_item.get("Id")
            assert test_id, "Campo 'Id' do primeiro item veio vazio/nulo"

        # -------------------------
        # GET BY ID (alvo do teste)
        # -------------------------
        with allure.step(f"Make GET request to /api/v1/amostragem-grupo-area/{test_id}"):
            response = page.get_by_id(test_id)
            req = response.request

            print("\n===== REQUEST =====")
            print("METHOD:", req.method)
            print("URL:", req.url)
            print("HEADERS:", req.headers)
            print("BODY:", req.body)

            print("\n===== RESPONSE =====")
            print("STATUS:", response.status_code)
            print("BODY:", response.text)

            attach_request("GET", f"/amostragem-grupo-area/{test_id}")
            attach_response(response, "Get By ID Response")

        with allure.step("Verify response status code"):
            assert response.status_code in [200, 404], (
                f"GET by ID deveria retornar 200 ou 404, retornou {response.status_code}"
            )

        # Se 200, valida contrato do payload
        if response.status_code == 200:
            with allure.step("Verify response body contract (when 200)"):
                try:
                    by_id_body = response.json()
                except Exception:
                    pytest.fail("GET by ID retornou 200, mas body não é JSON")

                # Alguns endpoints retornam objeto direto; outros podem retornar wrapper.
                # Aqui validamos o mínimo esperado: um dict (direto ou em 'Dados') com Id e campos principais.
                assert isinstance(by_id_body, dict), (
                    f"GET by ID deveria retornar um objeto JSON (dict), retornou: {type(by_id_body)}"
                )
                payload = by_id_body.get("Dados") if isinstance(by_id_body.get("Dados"), dict) else by_id_body
                assert "Id" in payload, "GET by ID (200) deveria conter a chave 'Id'"
                assert payload.get("Id") == test_id, (
                    f"GET by ID deveria retornar Id={test_id}, retornou {payload.get('Id')}"
                )

                # Campos comuns (ajuste se o endpoint não devolver algum deles)
                for key in [
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
                ]:
                    assert key in payload, f"GET by ID (200) deveria conter a chave '{key}'"
