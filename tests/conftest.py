import pytest
from fastapi.testclient import TestClient

from src.server import app


@pytest.fixture(scope="module")
def client():
    """Create a TestClient for all tests"""
    with TestClient(app) as test_client:
        yield test_client
