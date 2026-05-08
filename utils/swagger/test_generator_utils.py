"""Test generator utilities."""

from pathlib import Path
from datetime import datetime


class TestFileGenerator:
    """Generate pytest test files from endpoint specifications."""

    def __init__(self, base_dir: Path = Path("tests")):
        self.base_dir = Path(base_dir)

    def generate_conftest_for_endpoint(self, endpoint_name: str, fields: dict) -> str:
        """Generate conftest.py content for an endpoint."""
        class_name = self._to_class_name(endpoint_name)

        content = f'''"""Fixtures for {endpoint_name} tests."""
import pytest
from tests.{endpoint_name}.page import (
    {class_name}CreateRequest,
    {class_name}UpdateRequest,
)


@pytest.fixture
def valid_{endpoint_name}_data():
    """Generate valid {endpoint_name} creation data."""
    return {{
        # Add fields based on your API requirements
        {self._generate_fixture_fields(fields)}
    }}


@pytest.fixture
def invalid_{endpoint_name}_data():
    """Generate invalid {endpoint_name} data (missing required fields)."""
    return {{}}


@pytest.fixture
def update_{endpoint_name}_data():
    """Generate {endpoint_name} update data."""
    return {{
        # Add updatable fields
    }}
'''
        return content

    def generate_page_models(self, endpoint_name: str, schema: dict) -> str:
        """Generate page.py with Pydantic models."""
        class_name = self._to_class_name(endpoint_name)
        fields = schema.get("properties", {})

        content = f'''"""Pydantic models for {endpoint_name} endpoint."""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class {class_name}Schema(BaseModel):
    """Response schema for {endpoint_name}."""
    id: int
{self._generate_model_fields(fields)}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class {class_name}CreateRequest(BaseModel):
    """Request schema for creating {endpoint_name}."""
{self._generate_request_fields(fields)}
    pass


class {class_name}UpdateRequest(BaseModel):
    """Request schema for updating {endpoint_name}."""
    # Make all fields optional for partial updates
{self._generate_update_fields(fields)}
    pass
'''
        return content

    def _to_class_name(self, name: str) -> str:
        """Convert snake_case to PascalCase."""
        return "".join(word.capitalize() for word in name.split("_"))

    def _generate_model_fields(self, properties: dict) -> str:
        """Generate Pydantic model fields."""
        if not properties:
            return ""
        
        fields = []
        for name, schema in properties.items():
            python_type = self._schema_to_python_type(schema)
            fields.append(f"    {name}: {python_type}")
        
        return "\n".join(fields)

    def _generate_fixture_fields(self, fields: dict) -> str:
        """Generate fixture data fields."""
        if not fields:
            return '"name": "Test Name",'
        
        lines = []
        for name, field_type in fields.items():
            value = self._generate_test_value(field_type)
            lines.append(f'        "{name}": {value},')
        
        return "\n".join(lines)

    def _generate_request_fields(self, properties: dict) -> str:
        """Generate request model fields."""
        if not properties:
            return "    name: str\n    description: Optional[str] = None"
        
        fields = []
        required = []  # Would need to check schema for required fields
        
        for name, schema in properties.items():
            python_type = self._schema_to_python_type(schema)
            if name not in required:
                python_type = f"Optional[{python_type}]"
            fields.append(f"    {name}: {python_type}")
        
        return "\n".join(fields) if fields else "    name: str"

    def _generate_update_fields(self, properties: dict) -> str:
        """Generate update model fields (all optional)."""
        if not properties:
            return "    name: Optional[str] = None"
        
        fields = []
        for name, schema in properties.items():
            python_type = self._schema_to_python_type(schema)
            fields.append(f"    {name}: Optional[{python_type}] = None")
        
        return "\n".join(fields) if fields else "    name: Optional[str] = None"

    def _schema_to_python_type(self, schema: dict) -> str:
        """Convert JSON schema type to Python type."""
        schema_type = schema.get("type", "str")

        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "List",
            "object": "dict",
        }

        python_type = type_map.get(schema_type, "Any")

        if schema_type == "array":
            items = schema.get("items", {})
            item_type = self._schema_to_python_type(items)
            python_type = f"List[{item_type}]"

        return python_type

    def _generate_test_value(self, field_type: str):
        """Generate a test value based on field type."""
        if "int" in field_type.lower():
            return "1"
        elif "float" in field_type.lower():
            return "1.0"
        elif "bool" in field_type.lower():
            return "True"
        elif "list" in field_type.lower():
            return "[]"
        elif "dict" in field_type.lower():
            return "{}"
        else:
            return '"test_value"'


if __name__ == "__main__":
    generator = TestFileGenerator()
    print(generator.generate_page_models("area", {"properties": {"name": {"type": "string"}}}))
