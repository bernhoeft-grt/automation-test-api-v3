"""API Client for making HTTP requests."""
import requests
from typing import Dict, Any, Optional
from config import API_BASE_URL, TIMEOUT, API_KEY
from utils.helpers import log_request_response


class APIClient:
    """Client for making API requests."""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
        if API_KEY:
            self.session.headers.update({"Authorization": f"Bearer {API_KEY}"})
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """Make HTTP request."""
        url = f"{self.base_url}{endpoint}"
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
            headers=request_headers,
            timeout=TIMEOUT
        )
        log_request_response(
            response=response,
            method=method,
            endpoint=endpoint,
            request_body=data,
            request_params=params,
            request_headers=request_headers,
        )
        return response
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """GET request."""
        return self._make_request("GET", endpoint, params=params, headers=headers)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """POST request."""
        return self._make_request("POST", endpoint, data=data, headers=headers)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """PUT request."""
        return self._make_request("PUT", endpoint, data=data, headers=headers)
    
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """PATCH request."""
        return self._make_request("PATCH", endpoint, data=data, headers=headers)
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """DELETE request."""
        return self._make_request("DELETE", endpoint, headers=headers)
