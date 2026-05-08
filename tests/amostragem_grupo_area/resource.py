"""Resource for AmostragemGrupoArea API."""
from typing import Optional, Dict, Any
from utils.api_client import APIClient


class AmostragemGrupoAreaResource:
    """Resource for AmostragemGrupoArea endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/amostragem-grupo-area"
    
    def get_all(self):
        """GET /api/v1/amostragem-grupo-area - Retorna Todas as Amostragem Grupo Area Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/amostragem-grupo-area/{id} - Retorna a Amostragem Grupo Area por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/amostragem-grupo-area - Cria uma Amostragem Grupo Area."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/amostragem-grupo-area/{id} - Atualiza uma Amostragem Grupo Area por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/amostragem-grupo-area/{id} - Excluir uma Amostragem Grupo Area por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")