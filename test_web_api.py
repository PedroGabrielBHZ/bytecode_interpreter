#!/usr/bin/env python3
"""
Test script for the web API endpoints.
"""

import requests
import json


def test_run_api():
    """Test the /api/run endpoint."""
    url = "http://localhost:5000/api/run"
    data = {"code": "PUSH 10\nPUSH 20\nADD\nPRINT\nHALT"}

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_optimize_api():
    """Test the /api/optimize endpoint."""
    url = "http://localhost:5000/api/optimize"
    data = {"code": "PUSH 10\nPUSH 20\nADD\nPUSH 5\nPOP\nPRINT\nHALT"}

    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_health():
    """Test the /health endpoint."""
    url = "http://localhost:5000/health"

    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Testing Web API Endpoints...")
    print("\n1. Testing /api/run:")
    test_run_api()

    print("\n2. Testing /api/optimize:")
    test_optimize_api()

    print("\n3. Testing /health:")
    test_health()
