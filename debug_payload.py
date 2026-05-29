#!/usr/bin/env python3
"""Debug script to test API payloads and see full error messages."""
import sys
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from config import API_BASE_URL
from utils.auth import login_and_get_token

# Get token
try:
    token = login_and_get_token()
    print(f"✓ Token obtained: {token[:50]}...")
except Exception as e:
    print(f"✗ Auth error: {e}")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
}

# Test endpoints
tests = [
    ("POST", "/avisos", {"titulo": "Test Aviso", "Descricao": "Test Description"}),
    ("POST", "/amostragem-grupo-area", {"nome": "Test Amostragem", "Descricao": "Test Description"}),
    ("POST", "/contratada", {"nome": "Test Contratada", "Descricao": "Test Description"}),
    ("POST", "/contrato", {"numero": "TEST-001", "Descricao": "Test Description"}),
]

for method, path, data in tests:
    url = API_BASE_URL + path
    print(f"\n{'='*60}")
    print(f"{method} {path}")
    print(f"Payload: {json.dumps(data, indent=2)}")
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, verify=False, timeout=10)
        else:
            response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        print(f"Status: {response.status_code}")
        try:
            resp_json = response.json()
            print(f"Response:\n{json.dumps(resp_json, indent=2)}")
        except:
            print(f"Response: {response.text[:800]}")
    except Exception as e:
        print(f"Error: {e}")
