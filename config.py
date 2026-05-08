"""Configuration module for API tests."""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://contractwebapi.stage.bernhoeft.com.br")
API_VERSION = os.getenv("API_VERSION", "v1")
TIMEOUT = int(os.getenv("TIMEOUT", "30"))
API_KEY = os.getenv("API_KEY", "")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "https://loginapi.stage.bernhoeft.com.br")
AUTH_ENDPOINT = os.getenv("AUTH_ENDPOINT", "/api/v1/Auth/Logar")
AUTH_TENANT_ID = os.getenv("AUTH_TENANT_ID", "")
AUTH_EMAIL = os.getenv("AUTH_EMAIL", "")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "")
AUTH_MFA = int(os.getenv("AUTH_MFA", "0"))

API_BASE_URL = f"{BASE_URL}/api/{API_VERSION}"
