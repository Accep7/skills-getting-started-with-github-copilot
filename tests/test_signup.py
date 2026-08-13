"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities."""

    def test_signup_success(self, client, sample_email):
        """Test successfully signing up for an activity."""
        activity_name = "Chess Club"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant(self, client, sample_email):
        """Test that signup actually adds the participant to the activity."""
        activity_name = "Chess Club"
        
        # Get initial participant count
        get_response = client.get("/activities")
        initial_count = len(get_response.json()[activity_name]["participants"])
        
        # Sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200
        
        # Verify participant was added
        get_response = client.get("/activities")
        new_count = len(get_response.json()[activity_name]["participants"])
        assert new_count == initial_count + 1
        assert sample_email in get_response.json()[activity_name]["participants"]

    def test_signup_nonexistent_activity(self, client, sample_email):
        """Test signing up for a non-existent activity returns 404."""
        response = client.post(
            "/activities/NonExistentActivity/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_email(self, client):
        """Test signing up with an email already registered returns 400."""
        activity_name = "Chess Club"
        # Use an email already in the activity
        duplicate_email = "michael@mergington.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_missing_email_parameter(self, client):
        """Test signup without email parameter."""
        activity_name = "Chess Club"
        response = client.post(f"/activities/{activity_name}/signup")
        
        # FastAPI will return 422 for missing required parameter
        assert response.status_code == 422

    def test_signup_missing_activity_name(self, client, sample_email):
        """Test signup with missing activity name in path."""
        response = client.post(
            "/activities//signup",  # Empty activity name
            params={"email": sample_email}
        )
        
        # This should be treated as a 404 (not found)
        assert response.status_code in [404, 422]

    def test_signup_empty_email(self, client):
        """Test signup with empty email parameter."""
        activity_name = "Chess Club"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": ""}
        )
        
        # Should either fail or accept empty string
        # Current implementation may accept it, but it's not ideal
        # This test documents the current behavior
        assert response.status_code in [200, 400, 422]

    def test_signup_special_characters_in_activity_name(self, client, sample_email):
        """Test signup with URL-encoded special characters in activity name."""
        # Chess Club has a space, it should be URL-encoded
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 200
        
    def test_signup_case_sensitivity(self, client, sample_email):
        """Test that activity name lookup is case-sensitive."""
        # Assuming activity names are case-sensitive
        response = client.post(
            "/activities/chess club/signup",  # lowercase
            params={"email": sample_email}
        )
        
        assert response.status_code == 404
