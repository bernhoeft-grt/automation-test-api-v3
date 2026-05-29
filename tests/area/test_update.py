"""Test PUT /api/v1/area/{id}."""
import pytest
import allure
from utils.helpers import (
    attach_response,
    attach_request,
    assert_object_payload_schema,
    assert_status_code,
    get_existing_resource_id,
)


@allure.epic("ContractWeb API")
@allure.feature("Area")
@allure.story("PUT /api/v1/area/{id}")
class TestUpdateArea:
    """Test PUT update Area."""
    
    @allure.title("Update Area")
    @pytest.mark.api
    def test_update(self, api_client):
        """Test updating Area."""
        from tests.area.resource import AreaResource
        
        page = AreaResource(api_client)
        
        test_id = get_existing_resource_id(page.get_all())
        data = {"nome": "Updated Area", "Descricao": "Updated Description"}
        with allure.step(f"Make PUT request to /api/v1/area/{test_id}"):
            response = page.update(test_id, data)
            attach_request("PUT", f"/area/{test_id}", data)
            attach_response(response, "Update Response")

        with allure.step("Verify response status code"):
            assert_status_code(response, 200)

        with allure.step("Validate response schema"):
            assert_object_payload_schema(response, required_keys=["Id"], expected_id=test_id)
