import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def pristine_activities():
    """Save and restore the in-memory activities before/after each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
