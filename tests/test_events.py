"""Tests for Events API."""
import pytest
import allure
from utils.helpers import attach_response, attach_request


@allure.epic("ContractWeb API")
@allure.feature("Events")
class TestEvents:
    """Test cases for Events endpoints."""
    
    @allure.story("POST /api/v1/events/{type}")
    @allure.title("Create Event")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_event(self, api_client):
        """Test creating an event."""
        event_type = "test"
        data = {
            "data": "test_data"
        }
        with allure.step(f"Make POST request to /api/v1/events/{event_type}"):
            response = api_client.post(f"/events/{event_type}", data=data)
            attach_request("POST", f"/events/{event_type}", data)
            attach_response(response, "Create Event Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]
    
    @allure.story("POST /api/v1/events/pre-process-status/{type}")
    @allure.title("Pre-process status event")
    @pytest.mark.api
    @pytest.mark.critical
    def test_pre_process_status(self, api_client):
        """Test pre-process status endpoint."""
        event_type = "test"
        data = {
            "ids": [1, 2, 3]
        }
        with allure.step(f"Make POST request to /api/v1/events/pre-process-status/{event_type}"):
            response = api_client.post(f"/events/pre-process-status/{event_type}", data=data)
            attach_request("POST", f"/events/pre-process-status/{event_type}", data)
            attach_response(response, "Pre-process Status Response")
        
        with allure.step("Verify response status code"):
            assert response.status_code in [200, 201]