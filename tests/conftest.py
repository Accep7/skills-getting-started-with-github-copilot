"""
Shared test configuration and fixtures for FastAPI app tests.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(scope="session")
def app_instance():
    """Provide the FastAPI app instance for tests."""
    return app


@pytest.fixture
def client(app_instance):
    """Provide a TestClient for making requests to the app."""
    return TestClient(app_instance)


@pytest.fixture
def original_activities():
    """Store the original activities state before each test."""
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities_after_test(original_activities):
    """
    Automatically reset the activities dict to its original state after each test.
    This ensures test isolation since the app uses a global in-memory dictionary.
    """
    yield
    # Clear current activities and restore original state
    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def sample_activity():
    """Provide a sample activity for testing."""
    return {
        "description": "Test Activity",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 5,
        "participants": ["test1@example.com", "test2@example.com"]
    }


@pytest.fixture
def sample_email():
    """Provide a sample email for testing."""
    return "newstudent@mergington.edu"
