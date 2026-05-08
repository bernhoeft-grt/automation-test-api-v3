"""Resource for Contratada API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class ContratadaResource:
    """Resource for Contratada endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/contratada"
    
    def get_all(self):
        """GET /api/v1/contratada - Retorna Todas as Contratadas Cadastradas."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/contratada/{id} - Retorna a Contratada por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/contratada - Cria uma Contratada."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/contratada/{id} - Atualiza uma Contratada por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def patch(self, id: int, data: Dict[str, Any]):
        """PATCH /api/v1/contratada/{id} - Alterar parcialmente uma Contratada por ID."""
        return self.api_client.patch(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/contratada/{id} - Excluir uma Contratada por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")