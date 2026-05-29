"""Authentication helpers for API tests."""
from typing import Any, Dict, Iterable

import requests

from config import AUTH_BASE_URL, AUTH_ENDPOINT, AUTH_MFA, AUTH_PASSWORD, AUTH_TENANT_ID, AUTH_EMAIL, TIMEOUT


def _iter_dict_values(obj: Any) -> Iterable[Dict[str, Any]]:
    """Yield nested dicts to search for auth tokens."""
    if isinstance(obj, dict):
        yield obj
        for value in obj.values():
            yield from _iter_dict_values(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_dict_values(item)


def _extract_token(payload: Dict[str, Any]) -> str:
    """Extract a bearer token from common response shapes."""
    token_keys = ("token", "accessToken", "access_token", "jwt", "bearer")
    for obj in _iter_dict_values(payload):
        for key in token_keys:
            value = obj.get(key)
            if isinstance(value, str) and value:
                return value
    raise ValueError(
        f"Token not found in auth response. Keys found: {list(payload.keys())} "
        f"Structure: {payload}"
    )


def login_and_get_token() -> str:
    """Authenticate and return a bearer token."""
    if not AUTH_EMAIL or not AUTH_PASSWORD or not AUTH_TENANT_ID:
        raise ValueError("Missing AUTH_EMAIL, AUTH_PASSWORD, or AUTH_TENANT_ID in environment.")

    url = f"{AUTH_BASE_URL}{AUTH_ENDPOINT}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "TenantId": AUTH_TENANT_ID,
        "X-Create-Token-Cookie": "false",
    }
    payload = {
        "email": AUTH_EMAIL,
        "senha": AUTH_PASSWORD,
        "tipoMfa": AUTH_MFA,
    }

    response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)

    try:
        body = response.json()
    except ValueError:
        body = None

    if response.ok:
        if body is None:
            raise ValueError("Login response did not contain JSON payload.")
        return _extract_token(body)

    messages = []
    if isinstance(body, dict):
        messages = body.get("mensagens") or []

    detail = "; ".join(messages) if messages else response.text
    if "TenantID Inválido" in detail:
        detail = f"{detail.rstrip('.')} - Check AUTH_TENANT_ID in .env."

    raise RuntimeError(f"Login failed ({response.status_code}): {detail}")
