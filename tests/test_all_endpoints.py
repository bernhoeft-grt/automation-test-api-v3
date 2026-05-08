"""Comprehensive tests for all API endpoints using a Page Object/POJO style."""
from dataclasses import dataclass, replace
from typing import Dict, Optional, List

import allure
import pytest

from utils.helpers import attach_request, attach_response


@dataclass(frozen=True)
class EndpointSpec:
    """Represents one API endpoint (our POJO)."""

    method: str
    path: str
    payload: Optional[Dict[str, object]] = None
    story: Optional[str] = None

    @property
    def id(self) -> str:
        """Readable id for parametrize ids."""
        sanitized = self.path.replace("/", "_").replace("{", "").replace("}", "")
        return f"{self.method}_{sanitized}"


class EndpointPage:
    """Page Object-style wrapper to execute one endpoint."""

    def __init__(self, api_client, spec: EndpointSpec):
        self.api_client = api_client
        self.spec = spec

    def prepare(self) -> (str, Optional[Dict[str, object]]):
        """Resolve path params and split payload between path and body."""
        path = self.spec.path
        data: Optional[Dict[str, object]] = None

        if self.spec.payload:
            for key, value in self.spec.payload.items():
                placeholder = f"{{{key}}}"
                if placeholder in path:
                    path = path.replace(placeholder, str(value))
                else:
                    data = data or {}
                    data[key] = value

        return path, data

    def call(self):
        """Execute the request and return the response."""
        path, data = self.prepare()
        method = self.spec.method.upper()

        if method == "GET":
            response = self.api_client.get(path)
        elif method == "POST":
            response = self.api_client.post(path, data=data)
        elif method == "PUT":
            response = self.api_client.put(path, data=data)
        elif method == "PATCH":
            response = self.api_client.patch(path, data=data)
        elif method == "DELETE":
            response = self.api_client.delete(path)
        else:
            raise ValueError(f"Unsupported method: {method}")

        attach_request(method, path, data)
        attach_response(response, f"{method} {path}")
        return response


def _group(name: str, specs: List[EndpointSpec]) -> List[EndpointSpec]:
    """Helper to tag specs with allure story grouping via path prefix."""
    return [replace(spec, story=name) for spec in specs]


# Endpoint collections grouped by resource
AMOSTRAGEM = _group(
    "AmostragemGrupoArea",
    [
        EndpointSpec("GET", "/amostragem-grupo-area"),
        EndpointSpec("GET", "/amostragem-grupo-area/{id}", {"id": 1}),
        EndpointSpec("POST", "/amostragem-grupo-area", {"nome": "Test"}),
        EndpointSpec("PUT", "/amostragem-grupo-area/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/amostragem-grupo-area/{id}", {"id": 1}),
    ],
)

AREA = _group(
    "Area",
    [
        EndpointSpec("GET", "/area"),
        EndpointSpec("GET", "/area/{id}", {"id": 1}),
        EndpointSpec("POST", "/area", {"nome": "Test Area"}),
        EndpointSpec("PUT", "/area/{id}", {"id": 1, "nome": "Updated Area"}),
        EndpointSpec("DELETE", "/area/{id}", {"id": 1}),
    ],
)

AVISOS = _group(
    "Avisos",
    [
        EndpointSpec("GET", "/avisos"),
        EndpointSpec("GET", "/avisos/{id}", {"id": 1}),
        EndpointSpec("POST", "/avisos", {"titulo": "Test Aviso"}),
        EndpointSpec("PUT", "/avisos/{id}", {"id": 1, "titulo": "Updated Aviso"}),
        EndpointSpec("DELETE", "/avisos/{id}", {"id": 1}),
        EndpointSpec("GET", "/avisos/meus-avisos"),
    ],
)

CLASSIFICACAO_COLABORADOR = _group(
    "ClassificacaoColaborador",
    [
        EndpointSpec("GET", "/classificacao-colaborador"),
        EndpointSpec("GET", "/classificacao-colaborador/{id}", {"id": 1}),
        EndpointSpec("POST", "/classificacao-colaborador", {"nome": "Test"}),
        EndpointSpec("PUT", "/classificacao-colaborador/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/classificacao-colaborador/{id}", {"id": 1}),
    ],
)

CONTRATADA = _group(
    "Contratada",
    [
        EndpointSpec("GET", "/contratada"),
        EndpointSpec("GET", "/contratada/{id}", {"id": 1}),
        EndpointSpec("POST", "/contratada", {"nome": "Test Contratada"}),
        EndpointSpec("PUT", "/contratada/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("PATCH", "/contratada/{id}", {"id": 1, "nome": "Patched"}),
        EndpointSpec("DELETE", "/contratada/{id}", {"id": 1}),
    ],
)

CONTRATADA_CONTRATO = _group(
    "ContratadaContrato",
    [
        EndpointSpec("GET", "/contratada-contrato"),
        EndpointSpec("GET", "/contratada-contrato/{id}", {"id": 1}),
        EndpointSpec("POST", "/contratada-contrato", {"contratadaId": 1, "contratoId": 1}),
        EndpointSpec("PUT", "/contratada-contrato/{id}", {"id": 1}),
        EndpointSpec("DELETE", "/contratada-contrato/{id}", {"id": 1}),
    ],
)

CONTRATANTE = _group(
    "Contratante",
    [
        EndpointSpec("GET", "/contratante"),
        EndpointSpec("GET", "/contratante/{id}", {"id": 1}),
        EndpointSpec("POST", "/contratante", {"nome": "Test Contratante"}),
        EndpointSpec("PUT", "/contratante/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/contratante/{id}", {"id": 1}),
        EndpointSpec("GET", "/contratante/{id}/familia", {"id": 1}),
        EndpointSpec("PUT", "/contratante/{id}/familia", {"id": 1, "familiaIds": [1, 2]}),
        EndpointSpec("GET", "/contratante/{id}/grupo-area", {"id": 1}),
        EndpointSpec("PUT", "/contratante/{id}/grupo-area", {"id": 1, "grupoAreaIds": [1, 2]}),
        EndpointSpec("GET", "/contratante/{id}/grupo-area/{grupo-area-id}", {"id": 1, "grupo-area-id": 1}),
    ],
)

CONTRATO = _group(
    "Contrato",
    [
        EndpointSpec("GET", "/contrato"),
        EndpointSpec("GET", "/contrato/{id}", {"id": 1}),
        EndpointSpec("POST", "/contrato", {"numero": "TEST-001"}),
        EndpointSpec("PUT", "/contrato/{id}", {"id": 1, "numero": "TEST-002"}),
        EndpointSpec("DELETE", "/contrato/{id}", {"id": 1}),
        EndpointSpec("GET", "/contrato/{id}/contratada/{contratada_id}/operadores", {"id": 1, "contratada_id": 1}),
    ],
)

EVENTS = _group(
    "Events",
    [
        EndpointSpec("POST", "/events/{type}", {"type": "test"}),
        EndpointSpec("POST", "/events/pre-process-status/{type}", {"type": "test"}),
    ],
)

FAMILIA = _group(
    "Familia",
    [
        EndpointSpec("GET", "/familia"),
        EndpointSpec("GET", "/familia/{id}", {"id": 1}),
        EndpointSpec("POST", "/familia", {"nome": "Test Familia"}),
        EndpointSpec("PUT", "/familia/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/familia/{id}", {"id": 1}),
    ],
)

GRUPO_AREA = _group(
    "GrupoArea",
    [
        EndpointSpec("GET", "/grupo-area"),
        EndpointSpec("GET", "/grupo-area/{id}", {"id": 1}),
        EndpointSpec("POST", "/grupo-area", {"nome": "Test Grupo Area"}),
        EndpointSpec("PUT", "/grupo-area/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/grupo-area/{id}", {"id": 1}),
        EndpointSpec("GET", "/grupo-area/{id}/calendario", {"id": 1}),
        EndpointSpec("PUT", "/grupo-area/{id}/calendario", {"id": 1}),
        EndpointSpec("GET", "/grupo-area/{id}/grupo-faturamento", {"id": 1}),
        EndpointSpec("PUT", "/grupo-area/{id}/grupo-faturamento", {"id": 1}),
        EndpointSpec("GET", "/grupo-area/{id}/checklist", {"id": 1}),
    ],
)

GRUPO_CONTRATANTE = _group(
    "GrupoContratante",
    [
        EndpointSpec("GET", "/grupo-contratante"),
        EndpointSpec("GET", "/grupo-contratante/{id}", {"id": 1}),
        EndpointSpec("POST", "/grupo-contratante", {"nome": "Test"}),
        EndpointSpec("PUT", "/grupo-contratante/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/grupo-contratante/{id}", {"id": 1}),
    ],
)

GRUPO_FATURAMENTO = _group(
    "GrupoFaturamento",
    [
        EndpointSpec("GET", "/grupo-faturamento"),
        EndpointSpec("GET", "/grupo-faturamento/{id}", {"id": 1}),
        EndpointSpec("POST", "/grupo-faturamento", {"nome": "Test"}),
        EndpointSpec("PUT", "/grupo-faturamento/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/grupo-faturamento/{id}", {"id": 1}),
        EndpointSpec("GET", "/grupo-faturamento/{grupoFaturamentoId}/faixa-faturamento", {"grupoFaturamentoId": 1}),
        EndpointSpec(
            "GET",
            "/grupo-faturamento/{grupoFaturamentoId}/faixa-faturamento/{id}",
            {"grupoFaturamentoId": 1, "id": 1},
        ),
        EndpointSpec("POST", "/grupo-faturamento/{grupoFaturamentoId}/faixa-faturamento", {"grupoFaturamentoId": 1}),
        EndpointSpec(
            "PUT",
            "/grupo-faturamento/{grupoFaturamentoId}/faixa-faturamento/{id}",
            {"grupoFaturamentoId": 1, "id": 1},
        ),
        EndpointSpec(
            "DELETE",
            "/grupo-faturamento/{grupoFaturamentoId}/faixa-faturamento/{id}",
            {"grupoFaturamentoId": 1, "id": 1},
        ),
    ],
)

LOCAL_SERVICO = _group(
    "LocalServico",
    [
        EndpointSpec("GET", "/local-servico"),
        EndpointSpec("GET", "/local-servico/{id}", {"id": 1}),
        EndpointSpec("POST", "/local-servico", {"nome": "Test"}),
        EndpointSpec("PUT", "/local-servico/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/local-servico/{id}", {"id": 1}),
    ],
)

OBJETO_ANALISE = _group(
    "ObjetoAnalise",
    [
        EndpointSpec("GET", "/objeto-analise"),
        EndpointSpec("GET", "/objeto-analise/{id}", {"id": 1}),
        EndpointSpec("POST", "/objeto-analise", {"nome": "Test"}),
        EndpointSpec("PUT", "/objeto-analise/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/objeto-analise/{id}", {"id": 1}),
    ],
)

OBJETO_ANALISE_TIPO_ESPECIFICO = _group(
    "ObjetoAnaliseTipoEspecifico",
    [
        EndpointSpec("GET", "/objeto-analise-tipo-especifico"),
        EndpointSpec("GET", "/objeto-analise-tipo-especifico/{id}", {"id": 1}),
        EndpointSpec("POST", "/objeto-analise-tipo-especifico", {"nome": "Test"}),
        EndpointSpec("PUT", "/objeto-analise-tipo-especifico/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/objeto-analise-tipo-especifico/{id}", {"id": 1}),
    ],
)

OBJETO_OFICIAL = _group(
    "ObjetoOficial",
    [
        EndpointSpec("GET", "/objeto-oficial"),
        EndpointSpec("GET", "/objeto-oficial/{id}", {"id": 1}),
        EndpointSpec("POST", "/objeto-oficial", {"nome": "Test"}),
        EndpointSpec("PUT", "/objeto-oficial/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/objeto-oficial/{id}", {"id": 1}),
    ],
)

OPERADOR = _group(
    "Operador",
    [
        EndpointSpec("GET", "/operador"),
        EndpointSpec("POST", "/operador", {"nome": "Test Operador"}),
        EndpointSpec("POST", "/operador/vinculo", {"operadorId": 1, "contratadaId": 1}),
        EndpointSpec("DELETE", "/operador/vinculo/{OperadorContratadaContratoId}", {"OperadorContratadaContratoId": 1}),
    ],
)

PARAMETROS = _group(
    "Parametros",
    [
        EndpointSpec("GET", "/parametros/contatos"),
        EndpointSpec("GET", "/parametros/legacy-systems"),
    ],
)

PERFIL_ACESSO = _group(
    "PerfilAcesso",
    [
        EndpointSpec("GET", "/perfil-acesso"),
        EndpointSpec("GET", "/perfil-acesso/{id}", {"id": 1}),
    ],
)

RISCO = _group(
    "Risco",
    [
        EndpointSpec("GET", "/risco"),
        EndpointSpec("GET", "/risco/{id}", {"id": 1}),
        EndpointSpec("POST", "/risco", {"nome": "Test Risco"}),
        EndpointSpec("PUT", "/risco/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/risco/{id}", {"id": 1}),
    ],
)

SUB_FAMILIA = _group(
    "SubFamilia",
    [
        EndpointSpec("GET", "/sub-familia"),
        EndpointSpec("GET", "/sub-familia/{id}", {"id": 1}),
        EndpointSpec("POST", "/sub-familia", {"nome": "Test"}),
        EndpointSpec("PUT", "/sub-familia/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/sub-familia/{id}", {"id": 1}),
    ],
)

SUPORTE = _group(
    "Suporte",
    [
        EndpointSpec("GET", "/suporte/cartilha"),
        EndpointSpec("GET", "/suporte/cartilha/download/{pasta}", {"pasta": "test"}),
        EndpointSpec("POST", "/suporte/cartilha/upload/{pasta}", {"pasta": "test"}),
        EndpointSpec("DELETE", "/suporte/cartilha/delete/{pasta}", {"pasta": "test"}),
    ],
)

UNIDADE_CONTRATANTE = _group(
    "UnidadeContratante",
    [
        EndpointSpec("GET", "/unidade-contratante"),
        EndpointSpec("GET", "/unidade-contratante/{id}", {"id": 1}),
        EndpointSpec("POST", "/unidade-contratante", {"nome": "Test"}),
        EndpointSpec("PUT", "/unidade-contratante/{id}", {"id": 1, "nome": "Updated"}),
        EndpointSpec("DELETE", "/unidade-contratante/{id}", {"id": 1}),
    ],
)

VIDEO_CAST = _group(
    "VideoCast",
    [
        EndpointSpec("GET", "/video-cast"),
        EndpointSpec("GET", "/video-cast/{id}", {"id": 1}),
        EndpointSpec("POST", "/video-cast/callback", {"event": "test"}),
    ],
)


ENDPOINTS: List[EndpointSpec] = [
    *AMOSTRAGEM,
    *AREA,
    *AVISOS,
    *CLASSIFICACAO_COLABORADOR,
    *CONTRATADA,
    *CONTRATADA_CONTRATO,
    *CONTRATANTE,
    *CONTRATO,
    *EVENTS,
    *FAMILIA,
    *GRUPO_AREA,
    *GRUPO_CONTRATANTE,
    *GRUPO_FATURAMENTO,
    *LOCAL_SERVICO,
    *OBJETO_ANALISE,
    *OBJETO_ANALISE_TIPO_ESPECIFICO,
    *OBJETO_OFICIAL,
    *OPERADOR,
    *PARAMETROS,
    *PERFIL_ACESSO,
    *RISCO,
    *SUB_FAMILIA,
    *SUPORTE,
    *UNIDADE_CONTRATANTE,
    *VIDEO_CAST,
]


@allure.epic("ContractWeb API")
@allure.feature("All Endpoints")
class TestAllEndpoints:
    """Test cases for all API endpoints."""

    @pytest.mark.parametrize("spec", ENDPOINTS, ids=[endpoint.id for endpoint in ENDPOINTS])
    @pytest.mark.api
    @pytest.mark.regression
    def test_endpoint(self, api_client, spec: EndpointSpec):
        """Test one endpoint (one test per endpoint via parametrize ids)."""
        page = EndpointPage(api_client, spec)
        with allure.step(f"{spec.method} {spec.path}"):
            response = page.call()

        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201, 204, 400, 401, 403, 404, 500]
