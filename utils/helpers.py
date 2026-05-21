"""Helper functions for tests."""
import json
from collections.abc import Iterable as IterableCollection
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


def assert_status_code(
    response,
    expected_status: int | IterableCollection[int],
    context: str = "Validate response status code",
) -> None:
    """Assert HTTP status code with request/response context."""
    if isinstance(expected_status, int):
        expected_statuses = [expected_status]
    else:
        expected_statuses = list(expected_status)

    with allure.step(context):
        _attach_assertion_details(
            expected=expected_statuses,
            actual=response.status_code,
            extra={"url": getattr(response.request, "url", None)},
        )
        if len(expected_statuses) == 1:
            assert response.status_code == expected_statuses[0], (
                f"Status code inesperado. Esperado {expected_statuses[0]}, recebido {response.status_code}"
            )
            return

        assert response.status_code in expected_statuses, (
            f"Status code inesperado. Esperado um de {expected_statuses}, recebido {response.status_code}"
        )


def assert_json_response(response, context: str = "Validate response JSON body") -> Any:
    """Assert response body is valid JSON and return decoded payload."""
    with allure.step(context):
        try:
            payload = response.json()
        except Exception as exc:
            pytest.fail(
                f"Response deveria retornar JSON válido.\n"
                f"Status: {response.status_code}\n"
                f"Body: {response.text[:500]}\n"
                f"Erro: {exc}"
            )
        return payload


def assert_paginated_list_response(
    response,
    item_keys: Optional[List[str]] = None,
    wrapper_keys: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Validate paginated list response schema and return items."""
    data = assert_json_response(response)
    keys = wrapper_keys or ["Dados", "QuantidadeTotal", "Paginas", "Quantidade", "Pagina"]

    assert_is_instance(data, dict, "GET_ALL deveria retornar um objeto JSON (dict)")
    for key in keys:
        assert_in(key, data, f"GET_ALL deveria conter a chave '{key}'")

    items = data.get("Dados")
    assert_is_instance(items, list, "GET_ALL -> 'Dados' deveria ser uma lista")

    if len(items) == 0:
        pytest.skip("GET_ALL retornou lista vazia em 'Dados' (sem dados no ambiente)")

    first_item = items[0]
    assert_is_instance(first_item, dict, "Primeiro item de 'Dados' deveria ser um objeto (dict)")
    if item_keys:
        for key in item_keys:
            assert_in(key, first_item, f"Item de 'Dados' deveria conter a chave '{key}'")

    return items


def assert_object_payload_schema(
    response,
    required_keys: Optional[List[str]] = None,
    expected_id: Any = None,
) -> Dict[str, Any]:
    """Validate object payload schema and return object payload."""
    payload = get_object_payload(response)
    assert_is_instance(payload, dict, "Payload deveria ser um objeto JSON (dict)")

    if required_keys:
        for key in required_keys:
            assert_in(key, payload, f"Payload deveria conter a chave '{key}'")

    if expected_id is not None:
        payload_id = payload.get("Id", payload.get("id"))
        assert_true(
            payload_id == expected_id,
            f"Payload deveria retornar Id={expected_id}, retornou {payload_id}",
            actual=payload_id,
            expected=expected_id,
        )

    return payload


def assert_delete_response(response) -> None:
    """Validate delete success responses."""
    assert_status_code(response, [200, 204], context="Verify delete response status code")
    if response.status_code == 204:
        assert_true(
            not response.text.strip(),
            "DELETE com 204 não deveria retornar body",
            actual=response.text,
            expected="empty body",
        )
        return

    if response.text.strip():
        assert_json_response(response, context="Validate delete response JSON body")


def get_existing_resource_id(response, id_keys: Optional[List[str]] = None) -> Any:
    """Extract an existing resource id from a successful GET_ALL response."""
    assert_status_code(response, 200, context="Verify GET_ALL response status code")
    items = assert_list_payload(response)
    if len(items) == 0:
        pytest.skip("GET_ALL retornou lista vazia (sem dados no ambiente)")

    keys = id_keys or ["Id", "id"]
    first_item = items[0]
    assert_is_instance(first_item, dict, "Primeiro item deveria ser um objeto (dict)")
    for key in keys:
        value = first_item.get(key)
        if value is not None:
            return value

    pytest.fail(f"Nenhum identificador encontrado usando as chaves {keys}")


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
