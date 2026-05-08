"""Resource for Contrato API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class ContratoResource:
    """Resource for Contrato endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/contrato"
    
    def get_all(self):
        """GET /api/v1/contrato - Retorna Todos os Contratos Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/contrato/{id} - Retorna o Contrato por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/contrato - Cria um Contrato."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/contrato/{id} - Atualiza um Contrato por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/contrato/{id} - Excluir um Contrato por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")
    
    def get_operadores(self, id: int, contratada_id: int):
        """GET /api/v1/contrato/{id}/contratada/{contratada_id}/operadores - Retorna Todos os Operadores da Contratada do Contrato Cadastrado."""
        return self.api_client.get(f"{self.base_path}/{id}/contratada/{contratada_id}/operadores")