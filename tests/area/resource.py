"""Resource for Area API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class AreaResource:
    """Resource for Area endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/area"
    
    def get_all(self):
        """GET /api/v1/area - Retorna Todas as Areas Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/area/{id} - Retorna a Area por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/area - Cria uma Area."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/area/{id} - Atualiza uma Area por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/area/{id} - Excluir uma Area por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")