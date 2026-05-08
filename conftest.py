"""Pytest configuration and fixtures."""
import os
import shutil
import subprocess
from pathlib import Path

import allure
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
    allure.dynamic.link(API_BASE_URL, name="API Base URL")
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach pytest failure details to Allure on setup/call/teardown failures."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        allure.attach(
            report.outcome.upper(),
            name="Test Outcome",
            attachment_type=allure.attachment_type.TEXT,
        )

    if report.failed:
        longrepr_text = report.longreprtext if hasattr(report, "longreprtext") else str(report.longrepr)
        allure.attach(
            longrepr_text,
            name=f"Pytest Failure ({report.when})",
            attachment_type=allure.attachment_type.TEXT,
        )

        captured_sections = []
        for section_name, section_content in report.sections:
            captured_sections.append(f"## {section_name}\n{section_content}")

        if captured_sections:
            allure.attach(
                "\n\n".join(captured_sections),
                name=f"Captured Output ({report.when})",
                attachment_type=allure.attachment_type.TEXT,
            )


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
