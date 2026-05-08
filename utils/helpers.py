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


def _attach_assertion_details(expected: Any = None, actual: Any = None, extra: Optional[Dict[str, Any]] = None) -> None:
    """Attach structured assertion context to Allure."""
    payload = {
        "expected": expected,
        "actual": actual,
    }
    if extra:
        payload.update(extra)

    allure.attach(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str),
        name="Assertion Details",
        attachment_type=allure.attachment_type.JSON,
    )


def assert_equal(actual: Any, expected: Any, message: str) -> None:
    """Assert equality with Allure step and structured context."""
    with allure.step(message):
        _attach_assertion_details(expected=expected, actual=actual)
        assert actual == expected, message


def assert_in(member: Any, container: Any, message: str) -> None:
    """Assert membership with Allure step and structured context."""
    with allure.step(message):
        _attach_assertion_details(expected="member should exist in container", actual=member)
        assert member in container, message


def assert_true(condition: bool, message: str, *, actual: Any = None, expected: Any = True) -> None:
    """Assert truthy condition with Allure step and structured context."""
    with allure.step(message):
        _attach_assertion_details(expected=expected, actual=actual if actual is not None else condition)
        assert condition, message


def assert_is_instance(value: Any, expected_type: Any, message: str) -> None:
    """Assert instance type with Allure step and structured context."""
    with allure.step(message):
        expected_name = getattr(expected_type, "__name__", str(expected_type))
        actual_name = type(value).__name__
        _attach_assertion_details(expected=expected_name, actual=actual_name)
        assert isinstance(value, expected_type), message


def assert_status_code(response, expected_statuses: List[int], context: str = "Validate response status code") -> None:
    """Assert HTTP status code with request/response context."""
    with allure.step(context):
        _attach_assertion_details(
            expected=expected_statuses,
            actual=response.status_code,
            extra={"url": getattr(response.request, "url", None)},
        )
        assert response.status_code in expected_statuses, (
            f"Status code inesperado. Esperado um de {expected_statuses}, recebido {response.status_code}"
        )


def validate_response_structure(response, expected_keys: list):
    """Validate that response contains expected keys."""
    data = response.json()
    for key in expected_keys:
        assert_in(key, data, f"Expected key '{key}' not found in response")


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
            assert_in(key, data, f"GET_ALL deveria conter a chave '{key}'")
        items = data.get("Dados")
    else:
        items = data

    assert_is_instance(items, list, "GET_ALL -> lista deveria ser do tipo list")
    if len(items) == 0:
        pytest.skip("GET_ALL retornou lista vazia (sem dados no ambiente)")

    first = items[0]
    assert_is_instance(first, dict, "Primeiro item deveria ser um objeto (dict)")
    if item_keys:
        for key in item_keys:
            assert_in(key, first, f"Item de lista deveria conter a chave '{key}'")


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
        assert_true(items is not None, "Response deveria conter uma lista em 'Dados' ou semelhante", actual=items)
    else:
        raise AssertionError("Response deveria ser lista ou dict com lista")

    assert_is_instance(items, list, "Payload deveria ser uma lista")
    return items
