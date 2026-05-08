"""Resource for Contratante API."""
from typing import Optional, Dict, Any, List
from utils.api_client import APIClient


class ContratanteResource:
    """Resource for Contratante endpoints."""
    
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.base_path = "/contratante"
    
    def get_all(self):
        """GET /api/v1/contratante - Retorna Todas as Contratante Cadastrados."""
        return self.api_client.get(self.base_path)
    
    def get_by_id(self, id: int):
        """GET /api/v1/contratante/{id} - Retorna a Contratante por ID."""
        return self.api_client.get(f"{self.base_path}/{id}")
    
    def create(self, data: Dict[str, Any]):
        """POST /api/v1/contratante - Cria uma Contratante."""
        return self.api_client.post(self.base_path, data=data)
    
    def update(self, id: int, data: Dict[str, Any]):
        """PUT /api/v1/contratante/{id} - Atualiza uma Contratante por ID."""
        return self.api_client.put(f"{self.base_path}/{id}", data=data)
    
    def delete(self, id: int):
        """DELETE /api/v1/contratante/{id} - Excluir uma Contratante por ID."""
        return self.api_client.delete(f"{self.base_path}/{id}")
    
    def get_familia(self, id: int):
        """GET /api/v1/contratante/{id}/familia - Retorna Lista com Familia ID atrelados a Contratante."""
        return self.api_client.get(f"{self.base_path}/{id}/familia")
    
    def update_familia(self, id: int, familia_ids: List[int]):
        """PUT /api/v1/contratante/{id}/familia - Atualiza Lista de Familia ID atrelados a Contratante."""
        return self.api_client.put(f"{self.base_path}/{id}/familia", data={"familiaIds": familia_ids})
    
    def get_grupo_area(self, id: int):
        """GET /api/v1/contratante/{id}/grupo-area - Retorna Lista com Grupo de Area atrelados a Contratante."""
        return self.api_client.get(f"{self.base_path}/{id}/grupo-area")
    
    def update_grupo_area(self, id: int, grupo_area_ids: List[int]):
        """PUT /api/v1/contratante/{id}/grupo-area - Atualiza Lista de Grupo de Area ID atrelados a Contratante."""
        return self.api_client.put(f"{self.base_path}/{id}/grupo-area", data={"grupoAreaIds": grupo_area_ids})
    
    def get_grupo_area_by_id(self, id: int, grupo_area_id: int):
        """GET /api/v1/contratante/{id}/grupo-area/{grupo-area-id} - Retorna Lista com Objetos de Mobilização do Grupo de Area atrelados a Contratante."""
        return self.api_client.get(f"{self.base_path}/{id}/grupo-area/{grupo_area_id}")