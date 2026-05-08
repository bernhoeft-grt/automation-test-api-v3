"""Resource for ClassificacaoColaborador API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class ClassificacaoColaboradorResource:
    """Resource for ClassificacaoColaborador endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/classificacao-colaborador"
    
    def get_all(self):
        """GET /api/v1/classificacao-colaborador - Retorna Todas as Classificações de Colaborador Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/classificacao-colaborador/{id} - Retorna a Classificação de Colaborador por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/classificacao-colaborador - Cria uma Classificação de Colaborador."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/classificacao-colaborador/{id} - Atualiza uma Classificação de Colaborador por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/classificacao-colaborador/{id} - Excluir uma Classificação de Colaborador por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")