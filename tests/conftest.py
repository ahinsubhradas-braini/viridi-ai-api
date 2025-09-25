import pytest
from faker import Faker
from fastapi.testclient import TestClient

from src.server import app


@pytest.fixture(scope="module")
def client():
    """Create a TestClient for all tests"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def translate_fake_request():
    faker = Faker("is_IS")

    return {
        "module_name": "product",
        "module_id": faker.uuid4(),
        "source_lang": "is",
        "target_lang": "en",
        "source_data": {"product_name": faker.word()},
    }
