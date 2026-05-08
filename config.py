"""Configuration module for API tests."""
import os
from dotenv import load_dotenv

load_dotenv()


def _get_int_env(name: str, default: int) -> int:
    """Return integer env var, tolerating empty values."""
    raw_value = os.getenv(name)
    if raw_value is None or raw_value.strip() == "":
        return default
    return int(raw_value)

BASE_URL = os.getenv("BASE_URL", "https://contractwebapi.stage.bernhoeft.com.br")
API_VERSION = os.getenv("API_VERSION", "v1")
TIMEOUT = _get_int_env("TIMEOUT", 30)
API_KEY = os.getenv("API_KEY", "")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "https://loginapi.stage.bernhoeft.com.br")
AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT", "/api/v1/Auth/Logar")
AUTH_TENANT_ID = os.getenv("AUTH_TENANT_ID", "")
AUTH_EMAIL = os.getenv("AUTH_EMAIL", "")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "")
AUTH_MFA = _get_int_env("AUTH_MFA", 0)

API_BASE_URL = f"{BASE_URL}/api/{API_VERSION}"
