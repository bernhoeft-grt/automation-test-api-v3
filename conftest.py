"""Pytest configuration and fixtures."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from utils.api_client import APIClient
from config import API_BASE_URL, API_KEY
from utils.auth import login_and_get_token


@pytest.fixture(scope="session")
def auth_token():
    """Get auth token once per test session."""
    if API_KEY:
        return API_KEY
    return login_and_get_token()


@pytest.fixture(scope="session")
def api_client(auth_token):
    """Create API client instance."""
    client = APIClient(API_BASE_URL)
    if auth_token:
        client.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    return client


@pytest.fixture(autouse=True)
def attach_base_url(api_client):
    """Attach base URL to Allure report."""
    import allure
    allure.dynamic.link(API_BASE_URL, name="API Base URL")
    yield


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate Allure report after test run (if Allure CLI is available)."""
    if os.getenv("ALLURE_AUTO_GENERATE", "1") != "1":
        return
    if shutil.which("allure") is None:
        return

    results_dir = Path(os.getenv("ALLURE_RESULTS_DIR", "allure-results"))
    report_dir = Path(os.getenv("ALLURE_REPORT_DIR", "allure-report"))
    if not results_dir.exists():
        return
    if not any(results_dir.iterdir()):
        return

    subprocess.run(
        ["allure", "generate", str(results_dir), "-o", str(report_dir), "--clean"],
        check=False,
    )
