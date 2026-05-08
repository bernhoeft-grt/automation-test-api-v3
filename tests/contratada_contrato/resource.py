"""Resource for ContratadaContrato API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class ContratadaContratoResource:
    """Resource for ContratadaContrato endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/contratada-contrato"
    
    def get_all(self):
        """GET /api/v1/contratada-contrato - Retorna Todas as Contratadas de um Contrato Cadastrado."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/contratada-contrato/{id} - Retorna a Contratada do Contrato por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/contratada-contrato - Cria uma Contratada para o Contrato."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/contratada-contrato/{id} - Atualiza uma Contratada de um Contrato por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/contratada-contrato/{id} - Excluir uma Contratada de um Contrato por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")