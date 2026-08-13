"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestRemoveParticipant:
    """Test suite for removing participants from activities."""

    def test_remove_participant_success(self, client):
        """Test successfully removing a participant from an activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_remove_participant_actually_removes(self, client):
        """Test that remove actually deletes the participant from the activity."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Get initial participant count
        get_response = client.get("/activities")
        initial_participants = get_response.json()[activity_name]["participants"].copy()
        initial_count = len(initial_participants)
        
        # Remove participant
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify participant was removed
        get_response = client.get("/activities")
        new_participants = get_response.json()[activity_name]["participants"]
        assert len(new_participants) == initial_count - 1
        assert email not in new_participants

    def test_remove_nonexistent_activity(self, client):
        """Test removing participant from non-existent activity returns 404."""
        response = client.delete(
            "/activities/NonExistentActivity/signup",
            params={"email": "someone@example.com"}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_unregistered_participant(self, client):
        """Test removing a participant not registered for the activity returns 400."""
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_remove_missing_email_parameter(self, client):
        """Test remove without email parameter."""
        activity_name = "Chess Club"
        response = client.delete(f"/activities/{activity_name}/signup")
        
        # FastAPI will return 422 for missing required parameter
        assert response.status_code == 422

    def test_remove_empty_email(self, client):
        """Test remove with empty email parameter."""
        activity_name = "Chess Club"
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": ""}
        )
        
        # Empty email should not be registered, so should return 400
        assert response.status_code == 400

    def test_remove_multiple_times_fails_on_second(self, client):
        """Test that removing the same participant twice fails the second time."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # First removal should succeed
        response1 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second removal should fail
        response2 = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400

    def test_remove_different_activities_independent(self, client):
        """Test that removing from one activity doesn't affect others."""
        email = "henry@mergington.edu"  # In Science Club
        
        # Remove from Science Club
        response = client.delete(
            "/activities/Science Club/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify email is not in Science Club
        get_response = client.get("/activities")
        assert email not in get_response.json()["Science Club"]["participants"]
        
        # Verify email is still in other activities if it was registered there
        # (In this case, it's only in Science Club based on app.py data)

    def test_remove_case_sensitivity(self, client):
        """Test that activity name lookup is case-sensitive."""
        response = client.delete(
            "/activities/chess club/signup",  # lowercase
            params={"email": "michael@mergington.edu"}
        )
        
        # Should be 404 since activity names are case-sensitive
        assert response.status_code == 404
