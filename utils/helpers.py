"""Helper functions for tests."""
import json
from typing import Any, Dict, Iterable, List, Optional

import allure
import pytest


def attach_response(response, name: str = "Response"):
    """Attach response to Allure report."""
    try:
        payload = response.json()
        content = json.dumps(payload, indent=2, ensure_ascii=False)
        attachment_type = allure.attachment_type.JSON
    except Exception:
        content = response.text
        attachment_type = allure.attachment_type.TEXT

    allure.attach(
        content,
        name=name,
        attachment_type=attachment_type
    )


def attach_request(method: str, url: str, data: Any = None, name: str = "Request"):
    """Attach request details to Allure report."""
    request_data = {
        "method": method,
        "url": url,
        "data": data
    }
    allure.attach(
        json.dumps(request_data, indent=2, ensure_ascii=False),
        name=name,
        attachment_type=allure.attachment_type.JSON
    )


def log_request_response(
    response,
    method: str,
    endpoint: str,
    request_body: Any = None,
    request_params: Any = None,
    request_headers: Any = None,
) -> None:
    """Attach request and response details to Allure report."""
    request_data = {
        "method": method,
        "url": response.request.url,
        "headers": dict(request_headers) if request_headers else None,
        "params": request_params,
        "body": request_body,
    }

    allure.attach(
        json.dumps(request_data, indent=2, ensure_ascii=False),
        name="HTTP Request",
        attachment_type=allure.attachment_type.JSON,
    )

    try:
        response_body = response.json()
    except Exception:
        response_body = response.text

    response_data = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response_body,
        "elapsed_seconds": response.elapsed.total_seconds(),
    }

    allure.attach(
        json.dumps(response_data, indent=2, ensure_ascii=False),
        name="HTTP Response",
        attachment_type=allure.attachment_type.JSON,
    )


def validate_response_structure(response, expected_keys: list):
    """Validate that response contains expected keys."""
    data = response.json()
    for key in expected_keys:
        assert key in data, f"Expected key '{key}' not found in response"


def _iter_dicts(value: Any) -> Iterable[Dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from _iter_dicts(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_dicts(item)


def get_list_payload(response) -> List[Dict[str, Any]]:
    """Extract list payload from common response shapes."""
    data = response.json()
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("Dados", "dados", "data", "Data"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def get_object_payload(response) -> Dict[str, Any]:
    """Extract object payload from common response shapes."""
    data = response.json()
    if isinstance(data, dict):
        for key in ("Dados", "dados", "data", "Data"):
            value = data.get(key)
            if isinstance(value, dict):
                return value
        return data
    return {}


def get_first_id(response, id_keys: Optional[List[str]] = None) -> Optional[Any]:
    """Return first item's id from a list response."""
    keys = id_keys or ["Id", "id"]
    items = get_list_payload(response)
    if not items:
        return None
    first = items[0]
    if isinstance(first, dict):
        for key in keys:
            value = first.get(key)
            if value:
                return value
    return None


def assert_list_schema(response, item_keys: Optional[List[str]] = None) -> None:
    """Validate list response schema (paged or raw list)."""
    try:
        data = response.json()
    except Exception as e:
        pytest.fail(
            f"GET_ALL deveria retornar JSON válido.\n"
            f"Status: {response.status_code}\n"
            f"Body: {response.text[:200]}\n"
            f"Erro: {str(e)}"
        )
    
    if isinstance(data, dict):
        for key in ["Dados", "QuantidadeTotal", "Paginas", "Quantidade", "Pagina"]:
            assert key in data, f"GET_ALL deveria conter a chave '{key}'"
        items = data.get("Dados")
    else:
        items = data

    assert isinstance(items, list), "GET_ALL -> lista deveria ser do tipo list"
    if len(items) == 0:
        pytest.skip("GET_ALL retornou lista vazia (sem dados no ambiente)")

    first = items[0]
    assert isinstance(first, dict), "Primeiro item deveria ser um objeto (dict)"
    if item_keys:
        for key in item_keys:
            assert key in first, f"Item de lista deveria conter a chave '{key}'"


def assert_list_payload(response) -> List[Any]:
    """Validate response has a list payload and return it."""
    data = response.json()
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = None
        for key in ("Dados", "dados", "data", "Data"):
            value = data.get(key)
            if isinstance(value, list):
                items = value
                break
        assert items is not None, "Response deveria conter uma lista em 'Dados' ou semelhante"
    else:
        raise AssertionError("Response deveria ser lista ou dict com lista")

    assert isinstance(items, list), "Payload deveria ser uma lista"
    return items
