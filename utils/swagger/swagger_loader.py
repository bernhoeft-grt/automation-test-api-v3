"""Swagger API specification loader and parser."""

import json
import os
from typing import Optional, Dict, Any
from urllib.parse import urljoin
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv


class SwaggerLoader:
    """Load and parse Swagger/OpenAPI specifications."""

    def __init__(self):
        load_dotenv()
        self.swagger_url = os.getenv(
            "SWAGGER_URL",
            "https://contractwebapi.stage.bernhoeft.com.br/api/v1/swagger.json",
        )
        self.spec = None
        self._cache = {}

    def load_from_env(self) -> Dict[str, Any]:
        """Load Swagger spec from URL in .env."""
        if self.spec:
            return self.spec

        try:
            if self.swagger_url.startswith("http"):
                response = requests.get(self.swagger_url, timeout=10)
                response.raise_for_status()
                content = response.text
            else:
                with open(self.swagger_url) as f:
                    content = f.read()

            try:
                self.spec = json.loads(content)
            except json.JSONDecodeError:
                self.spec = yaml.safe_load(content)

            return self.spec
        except Exception as e:
            print(f"Error loading Swagger: {e}")
            return {}

    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load Swagger from local file."""
        try:
            with open(file_path) as f:
                if file_path.endswith(".json"):
                    self.spec = json.load(f)
                else:
                    self.spec = yaml.safe_load(f)
            return self.spec
        except Exception as e:
            print(f"Error loading from {file_path}: {e}")
            return {}

    def load_from_url(self, url: str) -> Dict[str, Any]:
        """Load Swagger from a specific URL."""
        self.swagger_url = url
        return self.load_from_env()

    def get_endpoints(self) -> list:
        """Get all endpoints from spec."""
        if not self.spec:
            self.load_from_env()

        endpoints = []
        paths = self.spec.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                if method.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                    continue

                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                })

        return endpoints

    def get_endpoint_details(self, path: str, method: str) -> Optional[Dict]:
        """Get detailed information about a specific endpoint."""
        if not self.spec:
            self.load_from_env()

        endpoint = self.spec.get("paths", {}).get(path, {}).get(method.lower())
        return endpoint

    def get_security_schemes(self) -> Dict[str, Any]:
        """Get authentication schemes."""
        if not self.spec:
            self.load_from_env()

        components = self.spec.get("components", {})
        return components.get("securitySchemes", {})

    def get_schemas(self) -> Dict[str, Any]:
        """Get all data schemas."""
        if not self.spec:
            self.load_from_env()

        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})

        if not schemas:
            schemas = self.spec.get("definitions", {})

        return schemas

    def resolve_ref(self, ref: str) -> Optional[Dict]:
        """Resolve a $ref reference."""
        if not self.spec:
            self.load_from_env()

        if ref in self._cache:
            return self._cache[ref]

        parts = ref.split("/")
        value = self.spec

        for part in parts:
            if part == "#":
                continue
            value = value.get(part, {})

        self._cache[ref] = value
        return value

    def get_api_info(self) -> Dict[str, Any]:
        """Get API info (title, version, etc.)."""
        if not self.spec:
            self.load_from_env()

        info = self.spec.get("info", {})
        return {
            "title": info.get("title", ""),
            "version": info.get("version", ""),
            "description": info.get("description", ""),
            "base_path": self.spec.get("basePath", ""),
            "host": self.spec.get("host", ""),
        }

    def export_endpoints_json(self, output_file: str = "endpoints.json"):
        """Export all endpoints to JSON file."""
        endpoints = self.get_endpoints()
        with open(output_file, "w") as f:
            json.dump(endpoints, f, indent=2)
        print(f"Exported {len(endpoints)} endpoints to {output_file}")

    def get_endpoint_by_tag(self, tag: str) -> list:
        """Get endpoints filtered by tag."""
        if not self.spec:
            self.load_from_env()

        endpoints = []
        paths = self.spec.get("paths", {})

        for path, methods in paths.items():
            for method, details in methods.items():
                endpoint_tags = details.get("tags", [])
                if tag in endpoint_tags:
                    endpoints.append({
                        "path": path,
                        "method": method.upper(),
                        "summary": details.get("summary", ""),
                    })

        return endpoints


if __name__ == "__main__":
    loader = SwaggerLoader()
    spec = loader.load_from_env()
    print(f"Loaded: {loader.get_api_info()}")
    endpoints = loader.get_endpoints()
    print(f"Found {len(endpoints)} endpoints")
