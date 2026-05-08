"""Resource for Avisos API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class AvisosResource:
    """Resource for Avisos endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/avisos"
    
    def get_all(self):
        """GET /api/v1/avisos - Retorna Todos os Avisos Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/avisos/{id} - Retorna um Aviso por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/avisos - Cria um Novo Aviso."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/avisos/{id} - Atualiza um Aviso por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/avisos/{id} - Excluir um Aviso por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")
    
    def get_meus_avisos(self):
        """GET /api/v1/avisos/meus-avisos - Retorna os Avisos do Operador Autenticado."""
        return self.api_client.get(f"{self.base_path}/meus-avisos")