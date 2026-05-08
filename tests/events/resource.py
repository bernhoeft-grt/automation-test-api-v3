"""Resource for Events API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class EventsResource:
    """Resource for Events endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/events"
    
    def create_event(self, event_type: str, data: Dict[str, Any]):
        """POST /api/v1/events/{type} - Cria um Evento."""
        return self.api_client.post(f"{self.base_path}/{event_type}", data=data)
    
    def pre_process_status(self, event_type: str, data: Dict[str, Any]):
        """POST /api/v1/events/pre-process-status/{type} - Requisita a busca e enfileiramento dos IDs de LCC que terão o status calculado."""
        return self.api_client.post(f"{self.base_path}/pre-process-status/{event_type}", data=data)